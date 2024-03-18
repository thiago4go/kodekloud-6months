# 📶 Service & Networking

## NodePort - Kubernetes Service&#x20;

It maps a port in the Node to the Pod

<figure><img src="../.gitbook/assets/image (11) (1).png" alt=""><figcaption></figcaption></figure>

```
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: NodePort
  ports:
  - targetPort: 80
    port: 80
    nodePort: 30008
  selector:
    app: myapp
    type: front-end
```

> This service will be bind to every pod that matchs the `selector` and it will rondomically serve a pod, serving as a loadbalace, It will also create the same service in every Node as well.
>
> Once created we usually do not need to make any changes on this Service

## ClusterIP

It is impossible to relay on IP address, since a pod livecycle is short and it portable



```
apiVersion: v1
kind: Service
metadata:
  name: back-end
spec:
  type: ClusterIP
  ports:
  - targetPort: 80
    port: 80
  selector:
    app: myapp
    type: back-end
```



## LoadBalance





## Network Polices

Traffic Rules\


<figure><img src="../.gitbook/assets/image (12) (1).png" alt=""><figcaption></figcaption></figure>

By default all pods in the node is AllAllow

To create and apply a Network Policy to a pod:

```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          name: api-pod
    ports:
    - protocol: TCP
      port: 3306

```

#### Explaining Ingress and Egress in Kubernetes Network Policies

In Kubernetes, network policies specify how pods are allowed to communicate with each other and with other network endpoints. They play a crucial role in securing your Kubernetes cluster by controlling the flow of traffic. There are two key concepts within network policies: Ingress and Egress.

* **Ingress**: Refers to incoming traffic to a pod. Ingress policies allow you to define rules to allow or block traffic coming into your pods from various sources. This is crucial for controlling access to services that need to be exposed externally or to limit access to a pod from other pods within the cluster.
* **Egress**: Refers to outgoing traffic from a pod. Egress policies help you define rules to allow or block traffic leaving your pods to different destinations. This can be important for preventing unnecessary access to external services or other pods and ensuring that pods can only communicate with authorized endpoints.

In summary, Ingress and Egress network policies enable fine-grained access control to and from the pods, enhancing the security posture of your Kubernetes deployments.

{% hint style="info" %}
Not all solutions that offers Networking to K8S support Network Policies
{% endhint %}

###

### Developing Network Policies

Our goal is to protect DB pod, from the DB pointofview it need an Ingress policy

```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          name: api-pod
      # without a dash, this is a combination with the previous rule "AND" Operator
      namespaceSelector:
        matchLabels:
          name: prod
    #with a dash makes another rule, "OR" operator   
    - ipBlock:
        cidr: 192.168.5.10/32 
     ports:
     - protocol: TCP
       port: 3306

 egress:
 - to:
     - ipBlock:
         cidr: 192.168.5.10/32
    ports:
    - protocol: TCP
      port: 3306
```

## Ingress

Complex setup\


<figure><img src="../.gitbook/assets/image (13) (1).png" alt=""><figcaption></figcaption></figure>



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

{% hint style="info" %}
Ingress resource -> annotations rewrite after path /something to what is set

```yaml
annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /

```
{% endhint %}



### FAQ – What is the rewrite-target option?

Different ingress controllers have different options that can be used to customise the way it works. NGINX Ingress controller has many options that can be seen [here](https://kubernetes.github.io/ingress-nginx/examples/). I would like to explain one such option that we will use in our labs. The [Rewrite](https://kubernetes.github.io/ingress-nginx/examples/rewrite/) target option.

&#x20;

Our `watch` app displays the video streaming webpage at `http://<watch-service>:<port>/`

Our `wear` app displays the apparel webpage at `http://<wear-service>:<port>/`

We must configure Ingress to achieve the below. When user visits the URL on the left, his request should be forwarded internally to the URL on the right. Note that the /watch and /wear URL path are what we configure on the ingress controller so we can forwarded users to the appropriate application in the backend. The applications don’t have this URL/Path configured on them:

&#x20;

`http://<ingress-service>:<ingress-port>/watch` –> `http://<watch-service>:<port>/`

`http://<ingress-service>:<ingress-port>/wear` –> `http://<wear-service>:<port>/`

&#x20;

Without the `rewrite-target` option, this is what would happen:

`http://<ingress-service>:<ingress-port>/watch` –> `http://<watch-service>:<port>/watch`

`http://<ingress-service>:<ingress-port>/wear` –> `http://<wear-service>:<port>/wear`

&#x20;

Notice `watch` and `wear` at the end of the target URLs. The target applications are not configured with `/watch` or `/wear` paths. They are different applications built specifically for their purpose, so they don’t expect `/watch` or `/wear` in the URLs. And as such the requests would fail and throw a `404` not found error.

&#x20;

To fix that we want to “ReWrite” the URL when the request is passed on to the watch or wear applications. We don’t want to pass in the same path that user typed in. So we specify the `rewrite-target` option. This rewrites the URL by replacing whatever is under `rules->http->paths->path` which happens to be `/pay` in this case with the value in `rewrite-target`. This works just like a search and replace function.

For example: `replace(path, rewrite-target)`

In our case: `replace("/path","/")`

&#x20;

```
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: test-ingress
  namespace: critical-space
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: /pay
        backend:
          serviceName: pay-service
          servicePort: 8282
```

&#x20;

In another example given [here](https://kubernetes.github.io/ingress-nginx/examples/rewrite/), this could also be:

`replace("/something(/|$)(.*)", "/$2")`

```
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
  name: rewrite
  namespace: default
spec:
  rules:
  - host: rewrite.bar.com
    http:
      paths:
      - backend:
          serviceName: http-svc
          servicePort: 80
        path: /something(/|$)(.*)
```

&#x20;



