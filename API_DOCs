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
