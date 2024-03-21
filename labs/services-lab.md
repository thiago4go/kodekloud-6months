# Services Lab

10 / 11

Create a new service to access the web application using the `service-definition-1.yaml` file\
`Name:` webapp-service\
`Type:` NodePort\
`targetPort:` 8080\
`port:` 8080\
`nodePort:` 30080\
`selector:`\
&#x20; `name:` simple-webapp



```
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: null
  labels:
    app: webapp-service
  name: webapp-service
spec:
  ports:
  - name: 8080-8080
    nodePort: 30080
    port: 8080
    protocol: TCP
    targetPort: 8080
  selector:
    name: simple-webapp
  type: NodePort
status:
  loadBalancer: {}
```

```
controlplane ~ ✖ k describe svc webapp-service 
Name:                     webapp-service
Namespace:                default
Labels:                   app=webapp-service
Annotations:              <none>
Selector:                 name=simple-webapp
Type:                     NodePort
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.43.202.92
IPs:                      10.43.202.92
Port:                     8080-8080  8080/TCP
TargetPort:               8080/TCP
NodePort:                 8080-8080  30080/TCP
Endpoints:                10.42.0.10:8080,10.42.0.11:8080,10.42.0.12:8080 + 1 more...
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>

controlplane ~ ➜  k get pods
NAME                                        READY   STATUS    RESTARTS   AGE
simple-webapp-deployment-7b447ccc74-4g269   1/1     Running   0          9m5s
simple-webapp-deployment-7b447ccc74-t7vj2   1/1     Running   0          9m5s
simple-webapp-deployment-7b447ccc74-h9vfm   1/1     Running   0          9m5s
simple-webapp-deployment-7b447ccc74-p4xsg   1/1     Running   0          9m5s
```





10 / 10

Create a network policy to allow traffic from the `Internal` application only to the `payroll-service` and `db-service`.

Use the spec given below. You might want to enable ingress traffic to the pod to test your rules in the UI.Also, ensure that you allow egress traffic to DNS ports TCP and UDP (port 53) to enable DNS resolution from the internal pod.



Policy Name: internal-policy

Policy Type: Egress

Egress Allow: payroll

Payroll Port: 8080

Egress Allow: mysql

MySQL Port: 3306



```
controlplane ~ ➜  cat internal-policy.yaml 
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: internal-policy
spec:
  egress:
  - to:
    - podSelector:
        matchLabels:
          name: payroll
    - podSelector:
        matchLabels:
          name: mysql
    ports:
    - port: 8080
      protocol: TCP
    - port: 3306
      protocol: TCP
    - port: 53
      protocol: UDP
    - port: 53
      protocol: TCP
  podSelector:
    matchLabels:
      name: internal
  policyTypes:
  - Egress
```



ingress&#x20;

```
controlplane ~ ✦ ➜  cat ingress.yaml 
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
  creationTimestamp: "2024-03-16T11:22:54Z"
  generation: 1
  name: ingress-wear-watch
  namespace: app-space
  resourceVersion: "834"
  uid: 989e9c06-0064-47a1-831d-594d8c9d8792
spec:
  rules:
  - http:
      paths:
      - backend:
          service:
            name: wear-service
            port:
              number: 8080
        path: /wear
        pathType: Prefix
      - backend:
          service:
            name: video-service
            port:
              number: 8080
        path: /stream
        pathType: Prefix
      - backend:
          service:
            name: food-service
            port:
              number: 8080
        path: /eat
        pathType: Prefix
```





create a new ingress resource into the correct namespace:

```
controlplane ~ ✦ ➜  cat pay-ingress.yaml 
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
  name: ingress-pay
  namespace: critical-space 
spec:
  rules:
  - http:
      paths:
      - backend:
          service: 
            name: pay-service 
            port:
              number: 8282
        path: /pay
        pathType: Prefix

controlplane ~ ✦ ➜  k -n critical-space replace --force -f pay-ingress.yaml 
```



Sample of Ingress-controler:

```
controlplane ~ ➜  cat ingress-controller.yaml 
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app.kubernetes.io/component: controller
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.1.2
    helm.sh/chart: ingress-nginx-4.0.18
  name: ingress-nginx-controller
  namespace: ingress-nginx
spec:
  replicas: 1
  minReadySeconds: 0
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app.kubernetes.io/component: controller
      app.kubernetes.io/instance: ingress-nginx
      app.kubernetes.io/name: ingress-nginx
  template:
    metadata:
      labels:
        app.kubernetes.io/component: controller
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/name: ingress-nginx
    spec:
      containers:
      - args:
        - /nginx-ingress-controller
        - --publish-service=$(POD_NAMESPACE)/ingress-nginx-controller
        - --election-id=ingress-controller-leader
        - --watch-ingress-without-class=true
        - --default-backend-service=app-space/default-http-backend
        - --controller-class=k8s.io/ingress-nginx
        - --ingress-class=nginx
        - --configmap=$(POD_NAMESPACE)/ingress-nginx-controller
        - --validating-webhook=:8443
        - --validating-webhook-certificate=/usr/local/certificates/cert
        - --validating-webhook-key=/usr/local/certificates/key
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: LD_PRELOAD
          value: /usr/local/lib/libmimalloc.so
        image: registry.k8s.io/ingress-nginx/controller:v1.1.2@sha256:28b11ce69e57843de44e3db6413e98d09de0f6688e33d4bd384002a44f78405c
        imagePullPolicy: IfNotPresent
        lifecycle:
          preStop:
            exec:
              command:
              - /wait-shutdown
        livenessProbe:
          failureThreshold: 5
          httpGet:
            path: /healthz
            port: 10254
            scheme: HTTP
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
        name: controller
        ports:
        - name: http
          containerPort: 80
          protocol: TCP
        - containerPort: 443
          name: https
          protocol: TCP
        - containerPort: 8443
          name: webhook
          protocol: TCP
        readinessProbe:
          failureThreshold: 3
          httpGet:
            path: /healthz
            port: 10254
            scheme: HTTP
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
        resources:
          requests:
            cpu: 100m
            memory: 90Mi
        securityContext:
          allowPrivilegeEscalation: true
          capabilities:
            add:
            - NET_BIND_SERVICE
            drop:
            - ALL
          runAsUser: 101
        volumeMounts:
        - mountPath: /usr/local/certificates/
          name: webhook-cert
          readOnly: true
      dnsPolicy: ClusterFirst
      nodeSelector:
        kubernetes.io/os: linux
      serviceAccountName: ingress-nginx
      terminationGracePeriodSeconds: 300
      volumes:
      - name: webhook-cert
        secret:
          secretName: ingress-nginx-admission

---
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: null
  labels:
    app.kubernetes.io/component: controller
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.1.2
    helm.sh/chart: ingress-nginx-4.0.18
  name: ingress-nginx-controller
  namespace: ingress-nginx
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
    nodePort: 30080
  selector:
    app.kubernetes.io/component: controller
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
  type: NodePort

```



7 / 8

Create the ingress resource to make the applications available at `/wear` and `/watch` on the Ingress service. Also, make use of `rewrite-target` annotation field: -

```
nginx.ingress.kubernetes.io/rewrite-target: /
```

`Ingress` resource comes under the `namespace` scoped, so don't forget to create the ingress in the `app-space` namespace.

```

controlplane ~ ➜  kubectl create ingress nota-ingress --class=default --rule="/wear=wear-service:8080" --rule="/watch=video-service:8080" \                         
  --annotation ingress.annotation1="nginx.ingress.kubernetes.io/rewrite-target: /"
ingress.networking.k8s.io/nota-ingress created
```

```
edit ingress

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
  creationTimestamp: "2024-03-16T19:58:28Z"
  generation: 2
  name: nota-ingress
  namespace: app-space
  resourceVersion: "5557"
  uid: c7427042-6662-4503-8b43-2d0e7f7d4768
spec:
  ingressClassName: default
  rules:
  - http:
      paths:
      - backend:
          service:
            name: wear-service
            port:
              number: 8080
        path: /wear
        pathType: Prefix
      - backend:
          service:
            name: video-service
            port:
              number: 8080
        path: /watch
        pathType: Prefix
status:
  loadBalancer: {}
```



<figure><img src="../.gitbook/assets/image (3) (1) (1).png" alt=""><figcaption></figcaption></figure>

{% code overflow="wrap" %}
```
k get deploy -n ingress-space

k expose deploy ingress-controller -n ingress-space --name=ingress --port=80 --target-port=80 --type=NodePort 
k edit svc ingress -n ingress-space
```
{% endcode %}
