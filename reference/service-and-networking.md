# 📶 Service & Networking

## NodePort - Kubernetes Service&#x20;

It maps a port in the Node to the Pod

<figure><img src="../.gitbook/assets/image (11).png" alt=""><figcaption></figcaption></figure>

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


<figure><img src="../.gitbook/assets/image (12).png" alt=""><figcaption></figcaption></figure>

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



