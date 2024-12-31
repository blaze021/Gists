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
