```
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: cluster-down-scaler
  namespace: default
spec:
  scaleTargetRef:
    name: my-deployment  # Replace with your deployment name
  minReplicaCount: 0  # No pods when the cluster is up
  maxReplicaCount: 5  # Scale up when the cluster is down
  cooldownPeriod: 30  # Wait time before scaling down
  pollingInterval: 15  # Check every 15 seconds
  triggers:
    - type: prometheus
      metadata:
        serverAddress: http://prometheus.default.svc:9090
        metricName: cluster_down
        query: "sum(up{cluster='connected-cluster'}) == 0"
        threshold: "1"  # Scale when the cluster is down

```

```
kubectl patch deployment <deployment-name> -p '{"spec":{"template":{"spec":{"containers":[{"name":"<container-name>","resources":{"requests":{"cpu":"<new-cpu-request>"},"limits":{"cpu":"<new-cpu-limit>"}}}]}}}}'
```

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-example
  labels:
    app: {{ .Chart.Name }}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {{ .Chart.Name }}
  template:
    metadata:
      labels:
        app: {{ .Chart.Name }}
    spec:
      initContainers:
        - name: init-script
          image: alpine:3.18
          command: ["sh", "-c"]
          args:
            - |
              echo "Running init container script..."
              echo "#!/bin/sh" > /shared/startup-init.sh
              echo "echo 'Init script executed'" >> /shared/startup-init.sh
              chmod +x /shared/startup-init.sh
          volumeMounts:
            - name: shared-data
              mountPath: /shared
      containers:
        - name: main-container
          image: alpine:3.18
          command: ["sh", "-c"]
          args:
            - |
              echo "Running main container script..."
              /shared/startup-init.sh
              echo "#!/bin/sh" > /shared/startup-main.sh
              echo "echo 'Main script executed'" >> /shared/startup-main.sh
              chmod +x /shared/startup-main.sh
              /shared/startup-main.sh
          volumeMounts:
            - name: shared-data
              mountPath: /shared
      volumes:
        - name: shared-data
          emptyDir: {}

```
