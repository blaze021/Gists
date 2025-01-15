Here’s an extended list of **50 examples** using the `lookup` function in Helm, including the original 20. These examples cover a wide range of Kubernetes resources and their fields.

---

### ConfigMap and Secret Examples

1. **ConfigMap Data**  
   ```yaml
   {{ (lookup "v1" "ConfigMap" .Release.Namespace "configmap-name").data.key }}
   ```

2. **Secret Data**  
   ```yaml
   {{ (lookup "v1" "Secret" .Release.Namespace "secret-name").data.password | b64dec }}
   ```

3. **ConfigMap Metadata Annotations**  
   ```yaml
   {{ (lookup "v1" "ConfigMap" .Release.Namespace "configmap-name").metadata.annotations["custom-annotation"] }}
   ```

4. **Secret Type**  
   ```yaml
   {{ (lookup "v1" "Secret" .Release.Namespace "secret-name").type }}
   ```

---

### Deployment Examples

5. **Deployment Labels**  
   ```yaml
   {{ (lookup "apps/v1" "Deployment" .Release.Namespace "deployment-name").metadata.labels.app }}
   ```

6. **Deployment Replicas**  
   ```yaml
   {{ (lookup "apps/v1" "Deployment" .Release.Namespace "deployment-name").spec.replicas }}
   ```

7. **Deployment Strategy**  
   ```yaml
   {{ (lookup "apps/v1" "Deployment" .Release.Namespace "deployment-name").spec.strategy.type }}
   ```

8. **Deployment Pod Selector**  
   ```yaml
   {{ (lookup "apps/v1" "Deployment" .Release.Namespace "deployment-name").spec.selector.matchLabels }}
   ```

---

### Pod and PodTemplate Examples

9. **Pod Status Phase**  
   ```yaml
   {{ (lookup "v1" "Pod" .Release.Namespace "pod-name").status.phase }}
   ```

10. **Pod IP**  
    ```yaml
    {{ (lookup "v1" "Pod" .Release.Namespace "pod-name").status.podIP }}
    ```

11. **Pod Node Name**  
    ```yaml
    {{ (lookup "v1" "Pod" .Release.Namespace "pod-name").spec.nodeName }}
    ```

12. **Pod Volumes**  
    ```yaml
    {{ (lookup "v1" "Pod" .Release.Namespace "pod-name").spec.volumes }}
    ```

13. **Pod Template Labels from Deployment**  
    ```yaml
    {{ (lookup "apps/v1" "Deployment" .Release.Namespace "deployment-name").spec.template.metadata.labels }}
    ```

---

### Service Examples

14. **Service Type**  
    ```yaml
    {{ (lookup "v1" "Service" .Release.Namespace "service-name").spec.type }}
    ```

15. **Service Annotations**  
    ```yaml
    {{ (lookup "v1" "Service" .Release.Namespace "service-name").metadata.annotations["service.beta.kubernetes.io/aws-load-balancer-backend-protocol"] }}
    ```

16. **Service Cluster IP**  
    ```yaml
    {{ (lookup "v1" "Service" .Release.Namespace "service-name").spec.clusterIP }}
    ```

17. **Service Ports**  
    ```yaml
    {{ (lookup "v1" "Service" .Release.Namespace "service-name").spec.ports }}
    ```

18. **Service External IPs**  
    ```yaml
    {{ (lookup "v1" "Service" .Release.Namespace "service-name").spec.externalIPs }}
    ```

---

### StatefulSet and DaemonSet Examples

19. **StatefulSet Replicas**  
    ```yaml
    {{ (lookup "apps/v1" "StatefulSet" .Release.Namespace "statefulset-name").spec.replicas }}
    ```

20. **DaemonSet Selector**  
    ```yaml
    {{ (lookup "apps/v1" "DaemonSet" .Release.Namespace "daemonset-name").spec.selector.matchLabels }}
    ```

21. **StatefulSet Service Name**  
    ```yaml
    {{ (lookup "apps/v1" "StatefulSet" .Release.Namespace "statefulset-name").spec.serviceName }}
    ```

22. **DaemonSet Update Strategy**  
    ```yaml
    {{ (lookup "apps/v1" "DaemonSet" .Release.Namespace "daemonset-name").spec.updateStrategy }}
    ```

---

### Job and CronJob Examples

23. **Job Completion Status**  
    ```yaml
    {{ (lookup "batch/v1" "Job" .Release.Namespace "job-name").status.succeeded }}
    ```

24. **Job Active Pods**  
    ```yaml
    {{ (lookup "batch/v1" "Job" .Release.Namespace "job-name").status.active }}
    ```

25. **CronJob Schedule**  
    ```yaml
    {{ (lookup "batch/v1" "CronJob" .Release.Namespace "cronjob-name").spec.schedule }}
    ```

26. **CronJob Suspend State**  
    ```yaml
    {{ (lookup "batch/v1" "CronJob" .Release.Namespace "cronjob-name").spec.suspend }}
    ```

---

### HorizontalPodAutoscaler Examples

27. **HorizontalPodAutoscaler Min Replicas**  
    ```yaml
    {{ (lookup "autoscaling/v1" "HorizontalPodAutoscaler" .Release.Namespace "hpa-name").spec.minReplicas }}
    ```

28. **HorizontalPodAutoscaler Max Replicas**  
    ```yaml
    {{ (lookup "autoscaling/v1" "HorizontalPodAutoscaler" .Release.Namespace "hpa-name").spec.maxReplicas }}
    ```

29. **HorizontalPodAutoscaler Current Metrics**  
    ```yaml
    {{ (lookup "autoscaling/v1" "HorizontalPodAutoscaler" .Release.Namespace "hpa-name").status.currentMetrics }}
    ```

---

### Ingress and NetworkPolicy Examples

30. **Ingress Rules**  
    ```yaml
    {{ (lookup "networking.k8s.io/v1" "Ingress" .Release.Namespace "ingress-name").spec.rules }}
    ```

31. **Ingress Annotations**  
    ```yaml
    {{ (lookup "networking.k8s.io/v1" "Ingress" .Release.Namespace "ingress-name").metadata.annotations }}
    ```

32. **NetworkPolicy Ingress Rules**  
    ```yaml
    {{ (lookup "networking.k8s.io/v1" "NetworkPolicy" .Release.Namespace "networkpolicy-name").spec.ingress }}
    ```

---

### PersistentVolume and PVC Examples

33. **PersistentVolumeClaim Status**  
    ```yaml
    {{ (lookup "v1" "PersistentVolumeClaim" .Release.Namespace "pvc-name").status.phase }}
    ```

34. **PersistentVolume Reclaim Policy**  
    ```yaml
    {{ (lookup "v1" "PersistentVolume" "" "pv-name").spec.persistentVolumeReclaimPolicy }}
    ```

35. **PersistentVolume Capacity**  
    ```yaml
    {{ (lookup "v1" "PersistentVolume" "" "pv-name").spec.capacity.storage }}
    ```

---

### ServiceAccount and RBAC Examples

36. **ServiceAccount Secrets**  
    ```yaml
    {{ (lookup "v1" "ServiceAccount" .Release.Namespace "serviceaccount-name").secrets[0].name }}
    ```

37. **RoleBinding Subjects**  
    ```yaml
    {{ (lookup "rbac.authorization.k8s.io/v1" "RoleBinding" .Release.Namespace "rolebinding-name").subjects }}
    ```

38. **ClusterRole Rules**  
    ```yaml
    {{ (lookup "rbac.authorization.k8s.io/v1" "ClusterRole" "" "clusterrole-name").rules }}
    ```

---

### Node and Endpoint Examples

39. **Node Allocatable Resources**  
    ```yaml
    {{ (lookup "v1" "Node" "" "node-name").status.allocatable }}
    ```

40. **Node Labels**  
    ```yaml
    {{ (lookup "v1" "Node" "" "node-name").metadata.labels }}
    ```

41. **Endpoints Subsets**  
    ```yaml
    {{ (lookup "v1" "Endpoints" .Release.Namespace "service-name").subsets }}
    ```

---

### Miscellaneous Examples

42. **CustomResourceDefinition Kind**  
    ```yaml
    {{ (lookup "apiextensions.k8s.io/v1" "CustomResourceDefinition" "" "custom-resource-name").spec.names.kind }}
    ```

43. **Event Messages**  
    ```yaml
    {{ (lookup "v1" "Event" .Release.Namespace "event-name").message }}
    ```

44. **Pod Disruption Budget**  
    ```yaml
    {{ (lookup "policy/v1" "PodDisruptionBudget" .Release.Namespace "pdb-name").spec.maxUnavailable }}
    ```

45. **API Service Group Version**  
    ```yaml
    {{ (lookup "apiregistration.k8s.io/v1" "APIService" "" "apiservice-name").spec.group }}
    ```

46. **StorageClass Parameters**  
    ```yaml
    {{ (lookup "storage.k8s.io/v1" "StorageClass" "" "storageclass-name").parameters }}
    ```

47. **Namespace Status**  
    ```yaml
    {{ (lookup "v1" "Namespace" "" "namespace-name").status.phase }}
    ```

48. **Pod Container Image**  
    ```yaml
    {{ (lookup "v1" "Pod" .Release.Namespace "pod-name").spec.containers[0].image }}
    ```

49. **Pod Restart Count**  
    ```yaml
    {{ (lookup "v1" "Pod" .Release.Namespace "pod-name").status.containerStatuses[0].restartCount }}
    ```

50. **Deployment Revision**  
    ```yaml
    {{ (lookup "apps/v1" "ControllerRevision" .Release.Namespace "deployment-name").metadata.labels["revision"] }}
    ```

---

These examples span most of the common Kubernetes resources and fields you would interact with. Let me know if you’d like explanations for any specific scenario!
