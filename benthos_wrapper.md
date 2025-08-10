Nice — below is an ordered, practical **guide + working Go code** for every component you asked for. It’s arranged so you can implement it step‑by‑step: REST wrapper (ingest), rate limiter, memory check, NATS JetStream producer, consumer/worker with memory guard + retry, plus helpful extras (Dockerfile, systemd, testing notes).

I’ll assume:

* Benthos exposes a PUT REST config endpoint (e.g. `http://benthos:4195/streams/<streamID>`).
* Each incoming request includes expected memory footprint either in header `X-Incoming-GB` (preferred) or in the JSON body as `mem_gb`. (Code supports header first, body fallback.)
* You’ll use NATS JetStream for persistence.

---

# Project layout

```
benthos-wrapper/
├─ cmd/server/main.go          # REST API + producer
├─ cmd/worker/main.go          # Worker consumer
├─ internal/ratelimit/limiter.go
├─ internal/mem/memguard.go
├─ internal/nats/client.go
├─ internal/worker/worker.go
├─ go.mod
├─ config.yaml
├─ Dockerfile
└─ docker-compose.yml          # optional: nats + benthos for dev
```

---

# 1) go.mod (dependencies)

```go
module github.com/yourorg/benthos-wrapper

go 1.20

require (
    github.com/cenkalti/backoff/v4 v4.1.2
    github.com/gin-gonic/gin v1.9.0
    github.com/nats-io/nats.go v1.17.0
    github.com/shirou/gopsutil/v3 v3.23.8
    golang.org/x/time v0.4.0
)
```

Adjust versions as needed.

---

# 2) config.yaml (example)

```yaml
nats_url: "nats://nats:4222"
benthos_base_url: "http://benthos:4195"
rate_limit_per_stream: # requests per second
  default: 1
  overrides:
    stream-a: 5
memory_limit_gb: 1.0   # minimum free GB required before processing an incoming request
worker_count: 4
```

---

# 3) internal/ratelimit/limiter.go

Per-stream rate limiters with TTL cleanup.

```go
package ratelimit

import (
    "sync"
    "time"

    "golang.org/x/time/rate"
)

type StreamLimiter struct {
    mu        sync.Mutex
    limiters  map[string]*entry
    defaultR  rate.Limit
    defaultB  int
    ttl       time.Duration
}

type entry struct {
    limiter *rate.Limiter
    last    time.Time
}

func New(defaultPerSec float64, burst int, ttl time.Duration) *StreamLimiter {
    return &StreamLimiter{
        limiters: make(map[string]*entry),
        defaultR: rate.Limit(defaultPerSec),
        defaultB: burst,
        ttl:      ttl,
    }
}

func (s *StreamLimiter) Get(streamID string) *rate.Limiter {
    s.mu.Lock()
    defer s.mu.Unlock()
    if e, ok := s.limiters[streamID]; ok {
        e.last = time.Now()
        return e.limiter
    }
    l := rate.NewLimiter(s.defaultR, s.defaultB)
    s.limiters[streamID] = &entry{limiter: l, last: time.Now()}
    return l
}

// Call periodically to remove old limiters
func (s *StreamLimiter) Cleanup() {
    s.mu.Lock()
    defer s.mu.Unlock()
    now := time.Now()
    for k, e := range s.limiters {
        if now.Sub(e.last) > s.ttl {
            delete(s.limiters, k)
        }
    }
}
```

Run a goroutine to call Cleanup every minute in `main`.

---

# 4) internal/mem/memguard.go

Memory-check helper using gopsutil. It returns available GB and boolean.

```go
package memguard

import (
    "context"
    "time"

    "github.com/shirou/gopsutil/v3/mem"
)

type Checker struct {
    // padding for safety (GB)
    SafetyPaddingGB float64
    // Optionally refresh interval caching
}

func New(safety float64) *Checker {
    return &Checker{SafetyPaddingGB: safety}
}

// HasEnough returns (availableGB, ok)
func (c *Checker) HasEnough(ctx context.Context, requiredGB float64) (float64, bool, error) {
    // small timeout to avoid hangs
    done := make(chan struct{})
    var v *mem.VirtualMemoryStat
    var err error
    go func() {
        v, err = mem.VirtualMemory()
        close(done)
    }()
    select {
    case <-done:
        if err != nil {
            return 0, false, err
        }
        availGB := float64(v.Available) / (1024.0 * 1024.0 * 1024.0)
        ok := availGB >= (requiredGB + c.SafetyPaddingGB)
        return availGB, ok, nil
    case <-ctx.Done():
        return 0, false, ctx.Err()
    case <-time.After(2 * time.Second):
        return 0, false, context.DeadlineExceeded
    }
}
```

---

# 5) internal/nats/client.go

NATS JetStream producer + helper subjects.

```go
package natsclient

import (
    "context"
    "time"

    "github.com/nats-io/nats.go"
)

type Client struct {
    nc *nats.Conn
    js nats.JetStreamContext
}

func New(natsURL string) (*Client, error) {
    nc, err := nats.Connect(natsURL, nats.MaxReconnects(-1))
    if err != nil {
        return nil, err
    }
    js, err := nc.JetStream()
    if err != nil {
        return nil, err
    }
    return &Client{nc: nc, js: js}, nil
}

func (c *Client) PublishStream(ctx context.Context, streamID string, data []byte) (*nats.PubAck, error) {
    subject := "benthos.stream." + streamID
    // ensure stream/consumer exists out of band in production, or create here if required
    return c.js.Publish(subject, data, nats.Context(ctx))
}

func (c *Client) Close() {
    if c.nc != nil && !c.nc.IsClosed() {
        c.nc.Close()
    }
}
```

Note: In production, create JetStream streams/consumers via `js.AddStream` with subjects like `benthos.stream.*` and durable consumers.

---

# 6) cmd/server/main.go — REST wrapper (producer)

This accepts PUT requests, rate-limits per stream, checks memory, and enqueues to NATS.

```go
package main

import (
    "context"
    "encoding/json"
    "io"
    "log"
    "net/http"
    "os"
    "strconv"
    "time"

    "github.com/gin-gonic/gin"
    "github.com/yourorg/benthos-wrapper/internal/memguard"
    "github.com/yourorg/benthos-wrapper/internal/natsclient"
    "github.com/yourorg/benthos-wrapper/internal/ratelimit"
)

type Config struct {
    NatsURL   string  `json:"nats_url"`
    SafetyGB  float64 `json:"safety_padding_gb"`
    DefaultRps float64 `json:"default_rps"`
}

func readConfig() Config {
    // minimal: read from env or file. For brevity use env.
    return Config{
        NatsURL:    getenv("NATS_URL", "nats://127.0.0.1:4222"),
        SafetyGB:   0.1,
        DefaultRps: 1,
    }
}

func getenv(k, def string) string {
    v := os.Getenv(k)
    if v == "" {
        return def
    }
    return v
}

func main() {
    cfg := readConfig()
    natsCli, err := natsclient.New(cfg.NatsURL)
    if err != nil {
        log.Fatalf("nats connect: %v", err)
    }
    defer natsCli.Close()

    limiter := ratelimit.New(cfg.DefaultRps, 5, 10*time.Minute)
    go func() {
        ticker := time.NewTicker(1 * time.Minute)
        for range ticker.C { limiter.Cleanup() }
    }()

    memChecker := memguard.New(cfg.SafetyGB)

    r := gin.Default()

    // PUT /streams/:streamID
    r.PUT("/streams/:streamID", func(c *gin.Context) {
        streamID := c.Param("streamID")
        l := limiter.Get(streamID)
        if !l.Allow() {
            c.JSON(http.StatusTooManyRequests, gin.H{"error": "rate limit"})
            return
        }

        data, err := io.ReadAll(c.Request.Body)
        if err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": "invalid body"})
            return
        }

        // get required GB from header, fallback to JSON field mem_gb
        var requiredGB float64
        if h := c.GetHeader("X-Incoming-GB"); h != "" {
            if v, err := strconv.ParseFloat(h, 64); err == nil {
                requiredGB = v
            }
        } else {
            var payload map[string]interface{}
            if err := json.Unmarshal(data, &payload); err == nil {
                if m, ok := payload["mem_gb"]; ok {
                    switch t := m.(type) {
                    case float64:
                        requiredGB = t
                    case string:
                        if v, err := strconv.ParseFloat(t, 64); err == nil {
                            requiredGB = v
                        }
                    }
                }
            }
        }
        if requiredGB <= 0 {
            // default small request
            requiredGB = 0.01
        }

        // quick check before enqueuing
        ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
        defer cancel()
        avail, ok, err := memChecker.HasEnough(ctx, requiredGB)
        if err != nil {
            log.Printf("mem check err: %v", err)
            // still allow enqueue so job can be deferred by worker
        } else if !ok {
            // respond accepted but queued; worker will defer if still over limit
            log.Printf("not enough memory (avail %.2f GB < needed %.2f), queueing", avail, requiredGB)
        }

        // annotate payload with requiredGB if not present
        // create envelope: { "payload": <raw-json-or-string>, "required_gb": <float> }
        envelope := map[string]interface{}{
            "required_gb": requiredGB,
            "payload":     json.RawMessage(data),
            "received_at": time.Now().UTC().Format(time.RFC3339),
        }
        envBytes, _ := json.Marshal(envelope)

        if _, err := natsCli.PublishStream(context.Background(), streamID, envBytes); err != nil {
            log.Printf("nats publish error: %v", err)
            c.JSON(http.StatusInternalServerError, gin.H{"error": "enqueue failed"})
            return
        }

        // 202 Accepted so client knows job is queued
        c.JSON(http.StatusAccepted, gin.H{"status": "queued"})
    })

    srvAddr := getenv("LISTEN_ADDR", ":8080")
    r.Run(srvAddr)
}
```

Notes:

* We respond `202 Accepted` when enqueued.
* Worker will perform final memory guard and defer (NakWithDelay) if necessary.

---

# 7) internal/worker/worker.go — consumer + retry + memory guard

```go
package worker

import (
    "bytes"
    "context"
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "time"

    "github.com/cenkalti/backoff/v4"
    "github.com/nats-io/nats.go"
    "github.com/yourorg/benthos-wrapper/internal/memguard"
    "github.com/yourorg/benthos-wrapper/internal/natsclient"
)

type Worker struct {
    Nats      *natsclient.Client
    BenthosBase string
    MemChecker *memguard.Checker
    HTTPClient *http.Client
}

func New(nc *natsclient.Client, benthosBase string, mc *memguard.Checker) *Worker {
    return &Worker{
        Nats: nc,
        BenthosBase: benthosBase,
        MemChecker: mc,
        HTTPClient: &http.Client{Timeout: 30 * time.Second},
    }
}

// StartConsumers starts 'n' parallel consumers
func (w *Worker) StartConsumers(streamID string, n int) error {
    subj := "benthos.stream." + streamID
    // create durable consumer (assumes JetStream stream exists)
    _, err := w.Nats.js.AddConsumer(streamID, &nats.ConsumerConfig{
        Durable:       "worker-durable-" + streamID,
        AckPolicy:     nats.AckExplicitPolicy,
        FilterSubject: subj,
        DeliverPolicy: nats.DeliverAllPolicy,
    })
    if err != nil && err != nats.ErrConsumerNameAlreadyInUse {
        // continue anyway, might already exist
        log.Printf("add consumer: %v", err)
    }

    _, err = w.Nats.js.Subscribe(subj, func(msg *nats.Msg) {
        go w.handleMsg(msg)
    }, nats.ManualAck())
    return err
}

func (w *Worker) handleMsg(msg *nats.Msg) {
    // parse envelope
    var env struct {
        RequiredGB float64          `json:"required_gb"`
        Payload    json.RawMessage  `json:"payload"`
    }
    if err := json.Unmarshal(msg.Data, &env); err != nil {
        log.Printf("bad message, acking: %v", err)
        msg.Ack()
        return
    }

    // Check memory before processing
    ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
    defer cancel()
    avail, ok, err := w.MemChecker.HasEnough(ctx, env.RequiredGB)
    if err != nil {
        log.Printf("mem check error: %v; proceeding to retry logic", err)
    }
    if !ok {
        // Not enough memory; requeue for later with backoff
        log.Printf("insufficient memory (avail %.2f GB < req %.2f), deferring", avail, env.RequiredGB)
        // Nak with delay so message becomes available later
        _ = msg.NakWithDelay(30 * time.Second)
        return
    }

    // Forward to Benthos with retry/backoff
    op := func() error {
        // build PUT URL (assumes payload has target stream; for simplicity we use the subject streamID)
        // If you need different mapping, include stream target in envelope.
        url := fmt.Sprintf("%s/streams/%s", w.BenthosBase, extractStreamFromSubject(msg.Subject))
        req, err := http.NewRequest("PUT", url, bytes.NewReader(env.Payload))
        if err != nil {
            return err
        }
        req.Header.Set("Content-Type", "application/json")
        resp, err := w.HTTPClient.Do(req)
        if err != nil {
            return err
        }
        defer resp.Body.Close()
        if resp.StatusCode >= 500 {
            return fmt.Errorf("server error %d", resp.StatusCode)
        } else if resp.StatusCode >= 400 {
            // treat 4xx as permanent failure — dead-letter
            body, _ := io.ReadAll(resp.Body)
            log.Printf("permanent failure from benthos: %d %s", resp.StatusCode, string(body))
            // ack to drop or route to DLQ
            return backoff.Permanent(fmt.Errorf("client error %d", resp.StatusCode))
        }
        return nil
    }

    bo := backoff.NewExponentialBackOff()
    bo.MaxElapsedTime = 5 * time.Minute

    if err := backoff.Retry(op, bo); err != nil {
        if _, ok := err.(*backoff.PermanentError); ok {
            // send to dead-letter subject
            dlq := "benthos.dlq"
            w.Nats.js.Publish(dlq, msg.Data) // ignore error for brevity
            msg.Ack()
            return
        }
        // if exhausted, we can NakWithDelay or move to DLQ
        log.Printf("processing failed after retries: %v — moving to DLQ", err)
        w.Nats.js.Publish("benthos.dlq", msg.Data)
        msg.Ack()
        return
    }

    // processed successfully
    msg.Ack()
}

func extractStreamFromSubject(subject string) string {
    // subject form: benthos.stream.<streamID>
    parts := strings.Split(subject, ".")
    if len(parts) >= 3 { return parts[2] }
    return "unknown"
}
```

Notes:

* Uses exponential backoff (cenkalti/backoff).
* Downgrades permanent 4xx to DLQ.
* Uses `NakWithDelay` to defer if memory insufficient.
* `MaxElapsedTime` controls retry window.

---

# 8) cmd/worker/main.go

Entrypoint to start worker(s).

```go
package main

import (
    "log"
    "os"
    "os/signal"
    "syscall"
    "time"

    "github.com/yourorg/benthos-wrapper/internal/memguard"
    "github.com/yourorg/benthos-wrapper/internal/natsclient"
    "github.com/yourorg/benthos-wrapper/internal/worker"
)

func getenv(k, def string) string {
    v := os.Getenv(k)
    if v == "" { return def }
    return v
}

func main() {
    nUrl := getenv("NATS_URL", "nats://127.0.0.1:4222")
    benthos := getenv("BENTHOS_BASE", "http://benthos:4195")
    streamID := getenv("STREAM_ID", "default")
    workerCount := 4

    nc, err := natsclient.New(nUrl)
    if err != nil {
        log.Fatalf("nats connect: %v", err)
    }
    defer nc.Close()

    memc := memguard.New(0.1)
    w := worker.New(nc, benthos, memc)
    if err := w.StartConsumers(streamID, workerCount); err != nil {
        log.Fatalf("start consumers: %v", err)
    }

    sig := make(chan os.Signal, 1)
    signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
    <-sig
    log.Println("shutting down")
    time.Sleep(1 * time.Second)
}
```

---

# 9) Dockerfile (single binary)

```dockerfile
FROM golang:1.20-alpine AS build
WORKDIR /src
COPY . .
RUN apk add --no-cache git
RUN go build -o /bin/benthos-wrapper ./cmd/server

FROM alpine:3.18
COPY --from=build /bin/benthos-wrapper /bin/benthos-wrapper
EXPOSE 8080
ENTRYPOINT ["/bin/benthos-wrapper"]
```

Build separate images for server and worker by building the appropriate cmd.

---

# 10) docker-compose (dev)

```yaml
version: '3.8'
services:
  nats:
    image: nats:2.9
    ports: ["4222:4222"]
    command: ["-js"]
  benthos:
    image: jeffail/benthos:4.14.0
    ports: ["4195:4195"]
    # supply a basic benthos config that accepts REST config for streams
  wrapper:
    build: .
    environment:
      - NATS_URL=nats://nats:4222
    ports:
      - "8080:8080"
```

---

# 11) systemd unit (example for worker)

If you run the worker as a service:

```
[Unit]
Description=Benthos Wrapper Worker
After=network.target

[Service]
ExecStart=/usr/local/bin/benthos-wrapper-worker --stream=stream-a
Restart=always
User=svcuser
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

---

# 12) Testing and QA

* Unit test mem guard by mocking `mem.VirtualMemory()` via an interface wrapper (not included above).
* Integration test: start docker-compose (nats + benthos + wrapper), send PUT with header `X-Incoming-GB: 0.01` and assert it results in a PUT to Benthos (use a simple test server instead of Benthos in CI to assert payload).
* Test rate limiting by sending bursts and validating `429` responses.

---

# 13) Operational notes / tuning

* `required_gb` must be provided or estimated — accurate numbers matter for correct gating.
* Memory check uses available memory on the host. For containerized workers, ensure cgroup memory metrics are visible or run workers with host access (or use cgroup-aware memory library).
* JetStream stream/consumer provisioning: in production create streams with subjects `benthos.stream.*` and appropriate storage/retention. Consider per-stream consumers with rate limits and max inflight.
* Consider exposing Prometheus metrics: queue length, messages processed, mem\_available\_gb, requeue counts, DLQ counts.
* For large payloads, use object storage: instead of pushing huge payloads into NATS consider storing the payload in S3/minio and push a small envelope with the object key + required\_gb to NATS.

---

# 14) Quick example request

```bash
curl -X PUT "http://wrapper:8080/streams/my-stream" \
  -H "Content-Type: application/json" \
  -H "X-Incoming-GB: 0.2" \
  -d '{"config": { "foo": "bar" }}'
# => 202 Accepted
```

---

If you want, I can:

* produce a ready-to-run **GitHub-ready repo** with the code files above,
* add **JetStream stream/consumer bootstrap code** to automatically create streams,
* add **Prometheus instrumentation** and sample Grafana dashboard panels,
* or convert to a single binary supporting both server & worker via commands/flags.

Which of those would you like next?
