```
I hope you're doing well.

I am writing to formally resign from my position as Associate at Morgan Stanley, with my last working day being June 6, 2025. I’ve recently been offered a new opportunity that aligns well with my long-term professional goals, and after thoughtful consideration, I have decided to move forward with this next step in my career.

This was not an easy decision, as working at Morgan Stanley has been a truly valuable and enriching experience. I’m incredibly grateful for the support, learning, and guidance I’ve received from both you and the broader team over the course of my time here.

Over the next 60 days, I’m committed to ensuring a smooth and seamless transition. Please let me know how I can best support the team in that process—whether it’s wrapping up ongoing work, documenting key processes, or assisting in onboarding someone new.

Thank you once again for everything. I look forward to staying in touch and wish Morgan Stanley continued success.

Warm regards,
```

```
I hope this message finds you well.

I am writing to formally resign from my position as Associate at Morgan Stanley, effective from today to my last working day as June 6, 2025. This decision has not been easy, as my time here has been immensely valuable and rewarding. However, I have been offered an opportunity that aligns closely with my long-term career goals, and after careful consideration, I have decided to pursue this new path.

I want to express my sincere gratitude for the support, mentorship, and opportunities I’ve received during my time at Morgan Stanley. Working with such a talented and driven team has significantly contributed to my professional growth, and I will carry those experiences with me into this next chapter.

Please let me know how I can ensure a smooth and seamless transition during my notice period. I am happy to assist in handing over responsibilities or training my replacement.

Thank you once again for the incredible experience. I hope to stay in touch and wish the team continued success in all future endeavors.
```


```

#!/bin/bash

set -e

# Function to display kustomizations
list_kustomizations() {
    echo "Fetching kustomizations in namespace: $NAMESPACE"
    flux get ks -n "$NAMESPACE"
}

# Function to suspend kustomizations
suspend_kustomizations() {
    for ks in "${SELECTED_KS[@]}"; do
        echo "Suspending $ks in namespace $NAMESPACE"
        flux suspend ks "$ks" -n "$NAMESPACE"
    done
}

# Function to update ConfigMap
update_configmap() {
    echo "Updating ConfigMap: $CONFIGMAP_NAME in namespace: $NAMESPACE"
    kubectl patch configmap "$CONFIGMAP_NAME" -n "$NAMESPACE" --type merge -p "$PATCH_DATA"
}

# Function to reconcile HelmRelease
reconcile_hr() {
    echo "Reconciling HelmRelease: $HR_NAME in namespace: $NAMESPACE"
    flux reconcile hr "$HR_NAME" -n "$NAMESPACE"
}

# User Input
read -p "Enter the namespace: " NAMESPACE
list_kustomizations
read -p "Enter the kustomizations to suspend (e.g., 1 2 3 or all): " SELECTION

# Fetch Kustomization names
MAPFILE -t KS_ARRAY < <(flux get ks -n "$NAMESPACE" | awk 'NR>1 {print $1}')
if [[ "$SELECTION" == "all" ]]; then
    SELECTED_KS=("${KS_ARRAY[@]}")
else
    IFS=' ' read -r -a INDEXES <<< "$SELECTION"
    for index in "${INDEXES[@]}"; do
        SELECTED_KS+=("${KS_ARRAY[$((index-1))]}")
    done
fi

suspend_kustomizations

# ConfigMap Update
read -p "Enter ConfigMap name to update: " CONFIGMAP_NAME
read -p "Enter JSON patch data for ConfigMap: " PATCH_DATA
update_configmap

# Reconcile HelmRelease
read -p "Enter HelmRelease name to reconcile: " HR_NAME
reconcile_hr

echo "Script execution completed successfully."


```

```
for entry in $(kubectl get pods -A --no-headers -o custom-columns="NAMESPACE:.metadata.namespace,NAME:.metadata.name"); do
  ns=$(echo "$entry" | cut -d' ' -f1)
  pod=$(echo "$entry" | cut -d' ' -f2)
  echo "Namespace: $ns, Pod: $pod"
done

```

```
kubectl get pods -A -o json | jq -r ' .items[] | .metadata.namespace as $ns | .metadata.name as $pod | [(.spec.containers[].resources.requests.cpu // "0")] as $cpu | $cpu | map(sub("m$"; "") | tonumber) | add as $totalCpu |  select($totalCpu > 3000) | "\($ns) \($pod) totalCpu)m"'

```

```
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace} {.metadata.name} {.spec.containers[*].resources.requests.cpu}{"\n"}{end}'

```

```
kubectl get pods -A -o json | jq -r '.items[] | {namespace: .metadata.namespace, name: .metadata.name, cpu: (.spec.containers[].resources.requests.cpu // "0")} | select(.cpu != "null") |  "\(.namespace) \(.name) \(.cpu)"' |   sed 's/m//g' | sort -k3 -nr | head -n 1
```

```
kubectl get deploy -A -o json | jq '[.items[] | {namespace: .metadata.namespace, name: .metadata.name, replicas: .status.replicas, updated: .status.updatedReplicas, available: .status.availableReplicas}]'
```

```
kubectl get pods -A -o json | jq '[.items[] | 
  {
    pod: .metadata.name, 
    environment: (
      (.metadata.name | split("-")) as $parts
      | if ($parts[1] | tonumber? // empty) then 
          $parts[0] + "-" + $parts[1] 
        else 
          $parts[1] 
        end
    )
  }
]'

```

```
kubectl get pods -A -o json | jq '[.items[] | 
  {
    pod: .metadata.name, 
    environment: (
      .metadata.name 
      | split("-") 
      | map(select(test("^(qa|prod|r[0-9]+)$"))) 
      | join("-")
    )
  }
]'

```

```
jq -R 'split(" ") | { (.[0]): { cluster_env: .[1] } }' < input.txt | jq -s add
```

```
kubectl get pods -A -o json | jq '[.items[] | 
  {
    namespace: .metadata.namespace, 
    pod: .metadata.name, 
    deployment: (.metadata.name | split("-")[:-1] | join("-")),
    main_container: (.spec.containers[0].name // null),
    resource_limit_cpu: (.spec.containers[0].resources.limits.cpu // null),
    resource_limit_memory: (.spec.containers[0].resources.limits.memory // null),
    resource_requests_cpu: (.spec.containers[0].resources.requests.cpu // null),
    resource_requests_memory: (.spec.containers[0].resources.requests.memory // null)
  }
]'

```

```
kubectl get pods -A -o json | jq '[.items[] | { 
  namespace: .metadata.namespace, 
  pod: .metadata.name, 
  deployment: (.metadata.name | match("^(?<deployment>.+-[^-]+)-[^-]+$") | .captures[0].string), 
  containers: [.spec.containers[] | {name: .name, resources: .resources}]
}]'


```

```
https://astaxie.gitbooks.io/build-web-application-with-golang/content/en/02.8.html
```

```
kubectl get deploy -A -o json | jq '[.items[] | {namespace: .metadata.namespace, deploy_name: .metadata.name, config_mode: (.spec.template.spec.containers[0].env[]? | select(.name=="CONFIG_MODE").value // null)}]'

```

```
kubectl get deploy -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{range .spec.template.spec.containers[*].env[?(@.name=="CONFIG_MODE")]}{.value}{"\n"}{end}{end}'
```

# **API Documentation for Kubernetes API Server Integration**

Welcome to the documentation for the Kubernetes API built using FastAPI. This API facilitates interaction with Kubernetes clusters by leveraging tools like `kubectl`, `helm`, and `fluxcd`. This document provides an overview of the API endpoints and how to use them effectively.

---

## **API Base URL**
All endpoints are accessible under the following base URL:
```
http://kube-api/swagger
```
You can explore and test the API through the interactive Swagger UI provided at this URL.

---

## **API Endpoints**

### **1. /flux/status/{cluster}/{namespace}**
**Description:**  
Retrieve information about kustomizations in a specified cluster and namespace.  

- **Method:** GET  
- **Parameters:**  
  - `cluster` (string): Name of the cluster.  
  - `namespace` (string): Target namespace.  

**Example:**  
```bash
GET /flux/status/my-cluster/default
```

---

### **2. /flux/suspended/{cluster}/{namespace}**
**Description:**  
Retrieve suspended kustomizations for a specified cluster and namespace.  

- **Method:** GET  
- **Parameters:**  
  - `cluster` (string): Name of the cluster.  
  - `namespace` (string): Target namespace.  

**Example:**  
```bash
GET /flux/suspended/my-cluster/default
```

---

### **3. /flux/ready_state/{cluster}/{namespace}**
**Description:**  
Retrieve kustomizations that are in a ready state for a specified cluster and namespace.  

- **Method:** GET  
- **Parameters:**  
  - `cluster` (string): Name of the cluster.  
  - `namespace` (string): Target namespace.  

**Example:**  
```bash
GET /flux/ready_state/my-cluster/default
```

---

### **4. /flux/logs/{log_level}/{cluster}/{namespace}**
**Description:**  
Fetch logs from Flux for a specific log level, cluster, and namespace.  

- **Method:** GET  
- **Parameters:**  
  - `log_level` (string): Log levels such as `debug`, `info`, or `error`.  
  - `cluster` (string): Name of the cluster.  
  - `namespace` (string): Target namespace.  

**Example:**  
```bash
GET /flux/logs/debug/my-cluster/default
```

---

### **5. /flux/system/{controller}/{cluster}**
**Description:**  
Retrieve information about controllers in the `flux-system` namespace for a specified cluster.  

- **Method:** GET  
- **Parameters:**  
  - `controller` (string): The controller name.  
  - `cluster` (string): Name of the cluster.  

**Example:**  
```bash
GET /flux/system/kustomize-controller/my-cluster
```

---

### **6. /kubectl/pod_status/{cluster}/{namespace}**
**Description:**  
Retrieve the status of pods for a specific cluster and namespace.  

- **Method:** GET  
- **Parameters:**  
  - `cluster` (string): Name of the cluster.  
  - `namespace` (string): Target namespace.  

**Example:**  
```bash
GET /kubectl/pod_status/my-cluster/default
```

---

### **7. /kubectl/deploy_status/{cluster}/{namespace}**
**Description:**  
Fetch deployment status for a specific cluster and namespace.  

- **Method:** GET  
- **Parameters:**  
  - `cluster` (string): Name of the cluster.  
  - `namespace` (string): Target namespace.  

**Example:**  
```bash
GET /kubectl/deploy_status/my-cluster/default
```

---

### **8. /kubectl/pod_limits/{cluster}/{namespace}**
**Description:**  
Retrieve pod resource limits and requests for a specific cluster and namespace.  

- **Method:** GET  
- **Parameters:**  
  - `cluster` (string): Name of the cluster.  
  - `namespace` (string): Target namespace.  

**Example:**  
```bash
GET /kubectl/pod_limits/my-cluster/default
```

---

### **9. /kubectl/pod_utils/{cluster}/{namespace}**
**Description:**  
Fetch pod utilization metrics for a specific cluster and namespace.  

- **Method:** GET  
- **Parameters:**  
  - `cluster` (string): Name of the cluster.  
  - `namespace` (string): Target namespace.  

**Example:**  
```bash
GET /kubectl/pod_utils/my-cluster/default
```

---

### **10. /dynamic_query**
**Description:**  
Execute a dynamic query based on a predefined configuration.  

- **Method:** GET  
- **Parameters:**  
  - `endpoint` (string): Endpoint key defined in the external configuration.  
  - `cluster` (string): Name of the cluster.  
  - `namespace` (string, optional): Target namespace (if required by the endpoint configuration).  

**Example:**  
To execute a query for `endpoint_1` across all namespaces:  
```bash
GET /dynamic_query?endpoint=endpoint_1&cluster=my-cluster
```

To query `endpoint_2` for a specific namespace:  
```bash
GET /dynamic_query?endpoint=endpoint_2&cluster=my-cluster&namespace=default
```

**Dynamic Query Configuration Format:**  
The configuration for dynamic queries is maintained in a JSON file. Below is an example structure:  
```json
{
  "endpoint_1": {
    "type": "df",
    "request_type": "GET",
    "auth_grp": "someauthgrp",
    "command": "kubectl get pods -A"
  },
  "endpoint_2": {
    "type": "json",
    "request_type": "GET",
    "auth_grp": "someauthgrp2",
    "command": "kubectl get configmaps -n {namespace} -o json"
  }
}
```

---

## **Authentication**
Ensure proper authentication by configuring your Kubernetes access appropriately. For certain endpoints, access might be restricted based on role or group membership, as defined in the `auth_grp` parameter of the dynamic query configuration.

---

## **Utilities Used**
- **kubectl**: Fetch Kubernetes cluster-related data.  
- **helm**: Interact with Helm charts and releases.  
- **fluxcd**: Query kustomizations, Helm releases, and controller logs.

---

This API is designed to simplify Kubernetes operations and streamline cluster management tasks. For detailed API schema and example responses, refer to the Swagger UI at `http://kube-api/swagger`.


To fetch a JSON file from an S3 store over HTTPS, load it into memory, and make it globally accessible across files in a FastAPI application, you can follow these steps:

### Step 1: Create a Config Loader
Create a utility to fetch the JSON from S3 and load it into memory. This can be placed in a file, such as `config_loader.py`.

```python
import requests
import json

# Global variable to hold the JSON data
config_data = None

def fetch_config(url: str):
    """Fetch JSON configuration from the given URL."""
    global config_data
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    config_data = response.json()
```

### Step 2: Initialize Config on App Startup
Use FastAPI's startup event to load the configuration at the start of the application. You can create the main application in `main.py`.

```python
from fastapi import FastAPI
from config_loader import fetch_config, config_data

app = FastAPI()

CONFIG_URL = "https://your-s3-store-url/config.json"

@app.on_event("startup")
async def load_config():
    """Load configuration on application startup."""
    fetch_config(CONFIG_URL)

@app.get("/config")
async def get_config():
    """Endpoint to return the loaded configuration."""
    return config_data
```

### Step 3: Access Config Data in Other Modules
In other parts of your application, you can directly import and use `config_data` from `config_loader.py`.

For example, in another module:

```python
from config_loader import config_data

def use_config():
    """Access global config data."""
    if config_data:
        print("Config Loaded:", config_data)
    else:
        print("Config not loaded yet!")
```

### Key Considerations
1. **Thread Safety**: If the config might change at runtime and you are running in a multi-threaded environment, consider using thread-safe techniques (e.g., locks) to ensure consistency.
2. **Error Handling**: Implement retries and error handling for the S3 fetch operation in case the network or S3 service is unavailable.
3. **Security**: Ensure the S3 URL and any credentials (if required) are securely stored, e.g., using environment variables.

Let me know if you need further assistance!

```
echo "abc 123!@#$%^&*()_+[]{}:/-" | sed -e 's/ /%20/g' -e 's/!/%21/g' -e 's/@/%40/g' -e 's/#/%23/g' -e 's/\$/%24/g' -e 's/&/%26/g' -e 's/(/%28/g' -e 's/)/%29/g' -e 's/*/%2A/g' -e 's/+/%2B/g' -e 's/,/%2C/g' -e 's/:/%3A/g' -e 's/;/%3B/g' -e 's/=/%3D/g' -e 's/?/%3F/g' -e 's/\[/%5B/g' -e 's/\]/%5D/g' -e 's/\//%2F/g' -e 's/-/%2D/g'

```

```
kubectl get pods --no-headers | awk '{age=$NF; if ((age ~ /m$/ && age+0 < 60) || (age ~ /h$/ && substr(age, 1, length(age)-1) * 60 < 60) || (age ~ /d$/ && substr(age, 1, length(age)-1) * 1440 < 60)) print $0}'
```
```
kubectl get pods --no-headers | awk '
function parse_age(age) {
    if (age ~ /d$/) {
        return substr(age, 1, length(age) - 1) * 1440;
    } else if (age ~ /h$/) {
        return substr(age, 1, length(age) - 1) * 60;
    } else if (age ~ /m$/) {
        return substr(age, 1, length(age) - 1);
    } else {
        return 0; # Default case for unknown formats
    }
}
{
    if (parse_age($NF) > 60) print $0;
}'

```
```
sum(kube_pod_container_resource_requests{resource="cpu"}) by (namespace, pod)
* on (namespace, pod) group_left(owner_name) kube_pod_owner{owner_kind="Deployment"} 
* 1000

```

```
"""kubectl get pods | awk 'NR==1 { 
        for (i=1; i<=NF; i++) header[i]=$i; 
        next 
     } 
     { 
        printf("{"); 
        for (i=1; i<=NF; i++) printf("\\"" header[i] "\\": \\"" $i "\\", "); 
        printf("}\\n"); 
     }' | sed 's/, }/}/' | jq -s ."""
```
```
#!/bin/bash

# Define the allowed cluster names
cluster_name=('cluster-name-1' 'cluster-2')

# Check if the cluster name passed as the first argument is in the list
if [[ ! " ${cluster_name[@]} " =~ " $1 " ]]; then
    echo "WRONG CLUSTER"
    exit 1
fi

echo "Cluster name $1 is valid."
# Continue with the rest of the script here if needed

```

```
kubectl get deployments --all-namespaces -o json | jq -r '
  .items[] | 
  select(.metadata.annotations."your-annotation-key" | not) | 
  .metadata.name + " in namespace " + .metadata.namespace'
```

```
kubectl get deployments --all-namespaces -o json | \
  grep -L '"your-annotation-key"' | \
  jq -r '.items[].metadata.name + " in namespace " + .items[].metadata.namespace'
```

```
kubectl get svc -o yaml | grep hostname: | awk '{ print $2 }' | xargs -I{} sh -c 'content=$(curl -s "https://{}/release.txt" || echo ""); if [[ -n "$content" ]]; then echo -e "{}\t$(echo "$content" | grep -i "sdk")"; fi'

```

```
#!/bin/bash

# Get the list of service names
services=$(kubectl get svc -o yaml | grep hostname: | awk '{ print $2 }')

# Output the header
echo -e "Service Name\tSDKs\n"

# Loop through each service
for service in $services; do
    # Attempt to fetch release.txt from the service
    sdk_versions=$(curl -s "https://${service}/release.txt" | grep -i "sdk")

    # Display the service name and SDKs (if found)
    if [[ -n "$sdk_versions" ]]; then
        echo -e "$service\t$sdk_versions"
    else
        echo -e "$service\t"
    fi
done

```

```
awk 'NR==1 { 
        for (i=1; i<=NF; i++) header[i]=$i; 
        next 
     } 
     { 
        printf("{"); 
        for (i=1; i<=NF; i++) printf("\"" header[i] "\": \"" $i "\", "); 
        printf("}\n"); 
     }' data.txt | sed 's/, }/}/' | jq -s .

```

```
{
    "/api/v1/data1": {
        "type": "json",
        "command": "curl -X GET http://localhost/api/v1/data1"
    },
    "/api/v1/data2": {
        "type": "df",
        "command": "curl -X GET http://localhost/api/v1/data2"
    },
    "/api/v1/data3": {
        "type": "json",
        "command": "curl -X GET http://localhost/api/v1/data3"
    },
    "/api/v1/data4": {
        "type": "df",
        "command": "curl -X GET http://localhost/api/v1/data4"
    },
    "/api/v1/data5": {
        "type": "json",
        "command": "curl -X GET http://localhost/api/v1/data5"
    },
    "/api/v1/data6": {
        "type": "df",
        "command": "curl -X GET http://localhost/api/v1/data6"
    },
    "/api/v1/data7": {
        "type": "json",
        "command": "curl -X GET http://localhost/api/v1/data7"
    },
    "/api/v1/data8": {
        "type": "df",
        "command": "curl -X GET http://localhost/api/v1/data8"
    },
    "/api/v1/data9": {
        "type": "json",
        "command": "curl -X GET http://localhost/api/v1/data9"
    },
    "/api/v1/data10": {
        "type": "df",
        "command": "curl -X GET http://localhost/api/v1/data10"
    }
}


```

```
curl 'http://xxx.com:9099/api/v1/query?query=up'
```

```
kubectl get configmaps -n default -o json | jq '.items[] | {Name: .metadata.name, Data: (.data | with_entries(select((.key | endswith(".json")) and (.value != null and .value != ""))))}'


```

```
import os
import subprocess
import json
import pandas as pd

# Function to get the ConfigMap data using kubectl
def get_configmap(configmap_name, namespace):
    # Use subprocess to run the kubectl command and get the configmap in JSON format
    result = subprocess.run(
        ["kubectl", "get", "configmap", configmap_name, "-n", namespace, "-o", "json"],
        stdout=subprocess.PIPE, text=True
    )
    # Parse the JSON output from kubectl
    configmap_data = json.loads(result.stdout)
    return configmap_data.get("data", {})  # Return only the 'data' field (key-value pairs)

# Function to save the data to files based on their content (JSON or XML)
def save_files_from_configmap(data):
    for key, value in data.items():
        # Check the content type based on the start of the value (JSON or XML)
        if value.strip().startswith("{"):
            filename = f"{key}.json"
            with open(filename, "w") as file:
                file.write(value)
            print(f"Saved JSON file: {filename}")
        elif value.strip().startswith("<"):
            filename = f"{key}.xml"
            with open(filename, "w") as file:
                file.write(value)
            print(f"Saved XML file: {filename}")
        else:
            print(f"Unknown format for {key}")

# Main function to extract and save files
def extract_configmap_files(configmap_name, namespace):
    data = get_configmap(configmap_name, namespace)
    
    if not data:
        print("No data found in the ConfigMap.")
        return
    
    # Use pandas to create a DataFrame if needed for further processing or analysis
    df = pd.DataFrame(data.items(), columns=['Filename', 'Content'])
    
    # Save files based on their content type
    save_files_from_configmap(data)
    
    # Optionally return the DataFrame
    return df

# Set your ConfigMap name and namespace
configmap_name = "<configmap-name>"
namespace = "<namespace>"

# Extract and save files from ConfigMap
df = extract_configmap_files(configmap_name, namespace)

# Display the DataFrame (optional)
print(df)

```

```
import time
import pytest
from timer import Timer  # Assuming your Timer class is in a file named timer.py

def test_timer_basic_functionality(capsys):
    with Timer() as t:
        time.sleep(1)

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the elapsed time is approximately 1 second
    assert pytest.approx(t.elapsed_time, rel=0.1) == 1
    # Check if the printed message contains "Time taken"
    assert "Time taken" in captured.out
    assert "seconds" in captured.out

def test_timer_with_exception(capsys):
    with pytest.raises(ValueError):
        with Timer() as t:
            time.sleep(0.5)
            raise ValueError("Test exception")
    
    # Capture the printed output
    captured = capsys.readouterr()

    # Even with an exception, ensure elapsed_time is set
    assert hasattr(t, 'elapsed_time')
    assert t.elapsed_time > 0

    # Check if the printed message contains "Time taken"
    assert "Time taken" in captured.out
    assert "seconds" in captured.out

```


Here’s a full week's vegetarian diet plan with approximately 2,500 calories per day in a single table:

| **Day**    | **Breakfast**                                                                                               | **Lunch**                                                                      | **Afternoon Snack**                                | **Dinner**                                                      | **Total Calories** |
|------------|--------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|---------------------------------------------------|-----------------------------------------------------------------|-------------------|
| **Monday** | Masala oats with milk, chopped apples, 1 banana + mixed nuts (20g)                                            | Dosa (3) with coconut chutney and sambar                                       | Sprouts salad + roasted peanuts                   | Boiled chana curry (1 cup) with brown rice (1.5 cups) + veggies | 2,500 kcal         |
| **Tuesday**| Whole grain toast (2 slices) with avocado spread, sliced tomatoes, mixed fruit salad + peanut butter (2 tbsp) | Idli (4) with tomato chutney and mixed vegetable curry                         | A glass of milk (250ml) + 1 banana                | Vegetable stir-fry (1.5 cups) with rice (1.5 cups)              | 2,500 kcal         |
| **Wednesday** | Banana smoothie (1 cup milk, 1 banana, ½ cup oats) + yogurt with honey + 1 apple                             | Rice (1.5 cups) with spicy chickpea curry (1 cup) + cucumber raita (1 cup)     | A small apple + almonds (20g)                    | Masala oats with mixed vegetables (1.5 cups)                    | 2,500 kcal         |
| **Thursday**| Whole grain bread (2 slices) with peanut butter, sliced bananas + cottage cheese with fruits (200g)          | Brown rice (1.5 cups) with mixed vegetable curry (1 cup)                       | Cottage cheese salad (paneer)                     | Dosa (3) with tomato chutney + sprouts salad                     | 2,500 kcal         |
| **Friday** | Apple slices with cottage cheese + Greek yogurt with apples + granola (2 tbsp)                                | Vegetable biryani (2 cups) with cucumber raita (1 cup)                         | A glass of milk (250ml) + roasted peanuts (20g)   | Boiled chana salad (1 cup) with cucumber, tomatoes + brown rice | 2,500 kcal         |
| **Saturday**| Masala oats (1.5 cups) with milk + oatmeal with bananas + honey                                              | Rice (1.5 cups) with spicy chickpea curry (1 cup) + stir-fried vegetables (1 cup) | A small apple + almonds (20g)                     | Idli (4) with coconut chutney and sambar                        | 2,500 kcal         |
| **Sunday** | Whole grain toast (2 slices) with avocado + veggie smoothie bowl (banana, yogurt, berries)                    | Rice (1.5 cups) with spicy chickpea curry (1 cup) + cucumber raita (1 cup)     | A glass of milk (250ml) + roasted nuts (20g)      | Boiled chana salad (1 cup) with cucumber, tomatoes + brown rice | 2,500 kcal         |

---

This table provides a complete vegetarian diet for the week with approximately 2,500 calories per day.
It looks like `script_a.sh` is getting stuck at `script_b.sh &`, which is intended to run in the background, but something in `script_b.sh` might still be causing the blocking behavior.

Here are a few things to check and try to resolve the issue:

### 1. **Redirect Output of `script_b.sh`:**
   The issue might be caused by `script_b.sh` still writing to standard output or standard error. By default, even when run in the background, the script's output may still tie up the terminal and prevent `script_a.sh` from continuing.

   Try redirecting both `stdout` and `stderr` to `/dev/null` to fully detach the background process:

   ```bash
   script_b.sh > /dev/null 2>&1 &
   ```

### 2. **Disown the Background Process:**
   After putting the process in the background, you may want to disown it so that it doesn't hold up the parent process (`script_a.sh`).

   ```bash
   script_b.sh > /dev/null 2>&1 &
   disown
   ```

   `disown` ensures that `script_a.sh` won't wait on `script_b.sh` to complete or interact with it.

### 3. **Check `script_b.sh` Logic:**
   Ensure that `script_b.sh`'s loop or any code within isn't hanging or misbehaving in such a way that it's affecting the parent script. If `script_b.sh` takes too long to initialize, it might also give the impression that `script_a.sh` is stuck.

### Example `script_a.sh`:

```bash
# code here 1...

# Run script_b.sh in background, with output and error redirected and process disowned
script_b.sh > /dev/null 2>&1 &

disown

# code here 2 ...
```

### Example `script_b.sh`:

```bash
while true
do
    # Some background task
    echo "Background process running"
    
    sleep 5
done
```

This approach should allow `script_a.sh` to continue after starting `script_b.sh` in the background without being blocked.
```

```
import subprocess
import json
import pandas as pd
from datetime import datetime, timezone

def get_pods_dataframe(namespace='default'):
    # Execute the kubectl command and capture the output in JSON format
    result = subprocess.run(['kubectl', 'get', 'pods', '-n', namespace, '-o', 'json'], stdout=subprocess.PIPE)
    pods_json = json.loads(result.stdout.decode('utf-8'))
    
    # Extract relevant data for the DataFrame
    pods_data = []
    for item in pods_json['items']:
        # Extract the required fields
        name = item['metadata']['name']
        ready = f"{sum(1 for cs in item['status']['containerStatuses'] if cs['ready'])}/{len(item['status']['containerStatuses'])}"
        status = item['status']['phase']
        restarts = sum(cs['restartCount'] for cs in item['status']['containerStatuses'])
        start_time = item['status'].get('startTime')
        
        # Calculate age in a human-readable format
        if start_time:
            start_time_dt = datetime.fromisoformat(start_time.rstrip('Z')).replace(tzinfo=timezone.utc)
            age = datetime.now(timezone.utc) - start_time_dt
            age_str = str(age).split('.')[0]  # Remove microseconds
        else:
            age_str = 'N/A'
        
        pods_data.append({
            'name': name,
            'ready': ready,
            'status': status,
            'restarts': restarts,
            'age': age_str
        })
    
    # Create and return the DataFrame
    return pd.DataFrame(pods_data)

# Example usage
df = get_pods_dataframe('default')
print(df)


```
```
import time

class Timer:
    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        print(f"Time taken: {self.elapsed_time} seconds")

# Using the context manager
with Timer():
    # This is the code block whose execution time is being measured
    for i in range(1000000):
        pass  # Replace with your actual code

```


```
#!/bin/bash

# Get the pod information in a raw format
pods_info=$(kubectl get pods -n default --no-headers)

# Initialize an empty JSON object
json_result='{ "result": ['

# Iterate over each line of the pod information
while IFS= read -r line; do
  # Extract the required fields using awk
  pod_name=$(echo $line | awk '{print $1}')
  ready=$(echo $line | awk '{print $2}')
  status=$(echo $line | awk '{print $3}')
  restarts=$(echo $line | awk '{print $4}')
  age=$(echo $line | awk '{print $5}')

  # Append to the JSON object
  json_result+='
    {
      "name": "'$pod_name'",
      "ready": "'$ready'",
      "status": "'$status'",
      "restarts": "'$restarts'",
      "age": "'$age'"
    },'
done <<< "$pods_info"

# Remove the trailing comma and close the JSON array
json_result=$(echo $json_result | sed 's/,$//')
json_result+=' ]}'

# Print the JSON object
echo "$json_result" | jq .

```

Creating a structured Flask API with the specified folder structure involves organizing your code in a modular way, making it easier to manage and maintain. Here’s a step-by-step guide with the example code for each file:

### Folder Structure
```
my_flask_app/
├── app.py
├── routes/
│   ├── __init__.py
│   ├── flux.py
│   ├── kube_ctl.py
│   └── helmctl.py
└── utils/
    ├── __init__.py
    └── util.py
```

### 1. app.py
This is the main file that initializes the Flask application and registers the blueprints.

```python
from flask import Flask
from routes.flux import flux_bp
from routes.kube_ctl import kube_ctl_bp
from routes.helmctl import helmctl_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(flux_bp, url_prefix='/flux')
app.register_blueprint(kube_ctl_bp, url_prefix='/kube')
app.register_blueprint(helmctl_bp, url_prefix='/helm')

if __name__ == '__main__':
    app.run(debug=True)
```

### 2. routes/flux.py
This file defines the routes related to Flux.

```python
from flask import Blueprint, jsonify

flux_bp = Blueprint('flux', __name__)

@flux_bp.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "Flux is running"})
```

### 3. routes/kube_ctl.py
This file defines the routes related to Kubernetes control.

```python
from flask import Blueprint, jsonify

kube_ctl_bp = Blueprint('kube_ctl', __name__)

@kube_ctl_bp.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "Kubernetes control is running"})
```

### 4. routes/helmctl.py
This file defines the routes related to Helm control.

```python
from flask import Blueprint, jsonify

helmctl_bp = Blueprint('helmctl', __name__)

@helmctl_bp.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "Helm control is running"})
```

### 5. utils/util.py
This file contains utility functions that can be used across different parts of the application.

```python
def common_util_function():
    return "This is a common utility function."
```

### 6. routes/__init__.py
This file makes the `routes` directory a package.

```python
# This file can be empty or you can initialize something if needed.
```

### 7. utils/__init__.py
This file makes the `utils` directory a package.

```python
# This file can be empty or you can initialize something if needed.
```

### Putting It All Together
1. **Run the Application**: To run the application, navigate to the directory containing `app.py` and execute the command:
    ```bash
    python app.py
    ```
2. **Access the Endpoints**:
    - Flux status: `http://127.0.0.1:5000/flux/status`
    - Kubernetes control status: `http://127.0.0.1:5000/kube/status`
    - Helm control status: `http://127.0.0.1:5000/helm/status`

This structure organizes the code into separate files for different routes and utilities, making it modular and easier to manage.


<br/>
<br/>
<br/>
<br/>


```
When Gremlin is installed into an SELinux system as a container (e.g Docker constainer, Kubernetes daemonset), the container runtime that manages Gremlin will run the Gremlin processes under the SELinux process label type container_t. Gremlin performs some actions that are not allowed by this process label:

    Install and manipulate files on the host: /var/lib/gremlin, /var/log/gremlin
    Load kernel modules for manipulating network transactions during network attacks, such as net_sch
    Communicate with the container runtime socket (e.g. /var/run/docker.sock) to launch containers that carry out attacks
    Read files in /proc

When you install Gremlin as root directly onto your host machines, you likely do not need to install any of these policies, as Gremlin should run under SELinux process label type unconfined_t.

To alleviate the privilege restrictions imposed on container_t, you can allow these privileges to container_t, providing Gremlin with everything it needs, but this would also give the same privileges to all other containers on your system, which is not ideal.

This project crates a new process label type gremlin.process and adds all the necessary privileges Gremlin needs, so that you can grant them to Gremlin only, and nothing else.

Gremlin builds on the SELinux inheritance patterns set out in containers/udica, providing Gremlin privileges on top of standard container privileges. See the policy here.

https://github.com/gremlin/selinux-policies
```


```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-policy
  namespace: your-namespace
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress



```
```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-from-browser
  namespace: your-namespace
spec:
  podSelector: {}
  ingress:
  - ports:
    - port: 80  # Allow incoming traffic on port 80 (HTTP)
    - port: 443 # Allow incoming traffic on port 443 (HTTPS)
    from:
    - podSelector: {}

```

```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-from-specific-namespaces
  namespace: your-namespace
spec:
  podSelector: {}
  ingress:
  - ports:
    - port: 80  # Allow incoming traffic on port 80 (HTTP)
    - port: 443 # Allow incoming traffic on port 443 (HTTPS)
    from:
    - podSelector: {}
      namespaceSelector:
        matchLabels:
          namespace-label-key: namespace-label-value
    - podSelector: {}
      namespaceSelector:
        matchLabels:
          another-namespace-label-key: another-namespace-label-value

```
```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-and-egress
  namespace: your-namespace
spec:
  podSelector: {}
  ingress:
  - ports:
    - port: 80  # Allow incoming traffic on port 80 (HTTP)
    - port: 443 # Allow incoming traffic on port 443 (HTTPS)
  egress:
  - to:
    - podSelector: {}
      namespaceSelector:
        matchLabels:
          namespace-label-key: namespace-label-value
    - podSelector: {}
      namespaceSelector:
        matchLabels:
          another-namespace-label-key: another-namespace-label-value

```

```
"############################################################################
"
" ooooo        ooooo ooooo      ooo ooooo     ooo ooooooo  ooooo 
" `888'        `888' `888b.     `8' `888'     `8'  `8888    d8'  
" 888          888   8 `88b.    8   888       8     Y888..8P    
" 888          888   8   `88b.  8   888       8      `8888'     
" 888          888   8     `88b.8   888       8     .8PY888.    
" 888       o  888   8       `888   `88.    .8'    d8'  `888b   
" o888ooooood8 o888o o8o        `8     `YbodP'    o888o  o88888o

" ooooo      ooo   .oooooo.   ooo        ooooo       .o.       oooooooooo.   
" `888b.     `8'  d8P'  `Y8b  `88.       .888'      .888.      `888'   `Y8b  
" 8 `88b.    8  888      888  888b     d'888      .8"888.      888      888 
" 8   `88b.  8  888      888  8 Y88. .P  888     .8' `888.     888      888 
" 8     `88b.8  888      888  8  `888'   888    .88ooo8888.    888      888 
" 8       `888  `88b    d88'  8    Y     888   .8'     `888.   888     d88' 
" o8o        `8   `Y8bood8P'  o8o        o888o o88o     o8888o o888bood8P'   
"
"############################################################################

" Vim configuration file "
"!!! COPY THIS FILE TO YOUR HOME FOLDER !!!"

" enable mouse support "
set mouse=a

" enable syntax "
syntax on

" enable line numbers "
set number

" highlight current line "
set cursorline
:highlight Cursorline cterm=bold ctermbg=black

" enable highlight search pattern "
set hlsearch

" enable smartcase search sensitivity "
set ignorecase
set smartcase

" Indentation using spaces "
" tabstop:	width of tab character
" softtabstop:	fine tunes the amount of whitespace to be added
" shiftwidth:	determines the amount of whitespace to add in normal mode
" expandtab:	when on use space instead of tab
" textwidth:	text wrap width
" autoindent:	autoindent in new line
set tabstop	=4
set softtabstop	=4
set shiftwidth	=4
set textwidth	=79
set expandtab
set autoindent

" show the matching part of pairs [] {} and () "
set showmatch

" remove trailing whitespace from Python and Fortran files "
autocmd BufWritePre *.py :%s/\s\+$//e
autocmd BufWritePre *.f90 :%s/\s\+$//e
autocmd BufWritePre *.f95 :%s/\s\+$//e
autocmd BufWritePre *.for :%s/\s\+$//e

" enable color themes "
if !has('gui_running')
	set t_Co=256
endif
" enable true colors support "
set termguicolors
" Vim colorscheme "
colorscheme desert

"-------------------------------------------------------------"
"Bonus. " Find & Replace (if you use the ignorecase, smartcase these are mandatory) "
"            :%s/<find>/<replace>/g   "replace global (e.g. :%s/mass/grass/g)"
"            :%s/<find>/<replace>/gc  "replace global with confirmation"
"            :%s/<find>/<replace>/gi  "replace global case insensitive"
"            :%s/<find>/<replace>/gI  "replace global case sensitive"
"            :%s/<find>/<replace>/gIc "replace global case sensitive with confirmation"

"        " Vim (book)marks "
"            mn     "replace n with a word A-Z or number 0-9"
"            :'n     "go to mark n"
"            :`.     "go to the last change"
"            :marks  "show all declared marks"
"            :delm n "delete mark n"

"        " Delete range selection "
"            :<line_number>,<line_number>d "(e.g. :2,10d deletes lines 2-10)"

"        " LaTeX shortcuts "
"            nnoremap <F1> :! pdflatex %<CR><CR>
"            nnoremap <F2> :! bibtex $(echo % \| sed 's/.tex$//') & disown<CR><CR>
"            nnoremap <F3> :! evince $(echo % \| sed 's/tex$/pdf/') & disown<CR><CR>
"            nnoremap <F4> :! rm *.log *.aux *.out *.blg & disown<CR><CR>
```




```
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-configmap
data:
  my-yaml-file.yaml: |
    apiVersion: ...
    # Add more YAML configurations here
```


```

apiVersion: batch/v1
kind: Job
metadata:
  name: my-job
spec:
  template:
    spec:
      containers:
      - name: my-container
        image: your-image-name:your-tag
        command: ["/bin/bash", "-c"]
        args:
        - |
          echo "Running command 1"
          kubectl apply -f /config/my-yaml-file.yaml
          command1
          echo "Running command 2"
          command2
          # Add more commands as needed
          wait
          echo "Another command"
          # Add more commands after the wait
        - |
          echo "Yet another command"
        volumeMounts:
        - name: config-volume
          mountPath: /config
      volumes:
      - name: config-volume
        configMap:
          name: my-configmap


```














































# Gists
Sure, here's a tabular summary of the weekly balanced vegetarian diet plan for a person with 105 kg weight:

| Day        | Breakfast                                           | Lunch                                 | Afternoon Snack     | Dinner                                        |
|------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------------|
| Monday     | Masala Oats with milk, chopped apples, and a banana | Dosa with coconut chutney and sambar  | Sprouts salad       | Boiled Chana curry with brown rice            |
| Tuesday    | Bread toast with avocado spread, sliced tomatoes, and a small bowl of mixed fruit salad (apples and bananas) | Idli with tomato chutney and a side of mixed vegetable curry | A glass of milk | Vegetable stir-fry with rice          |
| Wednesday  | Banana smoothie made with milk, a handful of oats, and a small bowl of yogurt with sliced bananas and a drizzle of honey | Rice with spicy chickpea curry (Chana) and cucumber raita | A small apple | Masala Oats with mixed vegetables       |
| Thursday   | Two whole grain bread slices with peanut butter, sliced bananas, and a small bowl of cottage cheese (paneer) with sliced fruits (e.g., apples, oranges) | Brown rice with mixed vegetable curry | A boiled egg (if you consume eggs) | Dosa with tomato chutney and a side of sprouts salad |
| Friday     | Apple slices with cottage cheese (paneer) and a small bowl of Greek yogurt with chopped apples and a sprinkle of granola | Vegetable biryani with raita | A glass of milk | Boiled Chana salad with cucumber, tomatoes, and lemon dressing |
| Saturday   | Masala Oats with mixed vegetables, milk, and a small bowl of oatmeal with sliced bananas and a drizzle of honey | Rice with spicy chickpea curry (Chana) and a side of stir-fried vegetables | A small apple | Idli with coconut chutney and a side of sambar |
| Sunday     | Choose a hearty breakfast or brunch of your choice that includes a mix of whole grains, fruits, vegetables, and protein (e.g., veggie omelette, whole grain toast with avocado spread, smoothie bowl) | Rice with spicy chickpea curry (Chana) and cucumber raita | A glass of milk | Boiled Chana salad with cucumber, tomatoes, and lemon dressing |

Remember to drink plenty of water throughout the day and adjust the portion sizes based on your individual dietary needs and activity levels. Enjoy a balanced and nutritious week!
