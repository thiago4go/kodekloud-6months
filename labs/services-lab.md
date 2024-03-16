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



### Ingress

Complex\


<figure><img src="../.gitbook/assets/image (13).png" alt=""><figcaption></figcaption></figure>



A kubernete cluster do not come with an Ingress Controler by default.

#### Lets use Nginx Controler

{% code overflow="wrap" %}
```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-ingress-controler
spec:
  replicas: 1
  seletor:
    matchLabels:
      name: nginx-ingress
    template:
      metadata:
        labels:
          name: nginx-ingress
        spec:
          containers:
            - name: nginx-ingress-controller
              image: quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.21.0
          args:
            - /nginx-ingress-controller 
            - --configmap=$(POD_NAMESPACE)/nginx-configuration
            
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
          ports:
            - name: http
              containerPort: 80
            - name: https
              containerPort: 443
  
```
{% endcode %}

{% hint style="info" %}
need to create also a ConfigMap
{% endhint %}

```
apiVersion: v1
kind: Service
metadata: 
  nmae: nginx-ingress
spec:
  type: NodePPort
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
    name: http
  - port: 443
    targetPort: 443
    protocol: TCP
    name: https
  selector:
    name: nginx-ingress
```

{% hint style="info" %}
Also need to create a ServiceAccount to set permissions
{% endhint %}

#### ingress resources

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-wear
spec:
  backend:
    serviceName: wear-service
    servicePort: 80
```

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-wear-watch
spec:
  rules:
  - http:
    paths:
    - path: /wear
      pathType: Prefix
      backend:
        service:
          name: wear-service
          port: 
            number: 80
    - path: /watch
      pathType: Prefix
      backend:
        service:
          name: watch-service
          port: 
            number: 80    
```

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-wear-watch
spec:
  rules:
  - host: wear.my-online-store.com
    http:
      paths:
      - backend:
          serviceName: wear-service
          servicePort: 80
  - host: watch.my-online-store.com
    http:
      paths:
      - backend: 
          serviceName: watch-service
          servicePort: 80    
```

{% code overflow="wrap" %}
```
kubectl create ingress <ingress-name> --rule="host/path=service:port"

kubectl create ingress ingress-test --rule="wear.my-online-store.com/wear*=wear-service:80"
```
{% endcode %}





ingress

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
