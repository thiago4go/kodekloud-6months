# Lab #9

3 / 8 Apply a label color=blue to node node01

```
k label nodes node01 color=blue
```

4/8 Create a new deployment named `blue` with the `nginx` image and 3 replicas.

{% code overflow="wrap" %}
```
k create deployment blue --image=nginx  --replicas=3
```
{% endcode %}



6 / 8 Set Node Affinity to the deployment to place the pods on `node01` only.

Name: blue

Replicas: 3

Image: nginx

NodeAffinity: requiredDuringSchedulingIgnoredDuringExecution

Key: color

value: blue

```
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: blue
  name: blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: blue
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: blue
    spec:
      affinity:
        nodeAffinity: 
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: color
                operator: In
                values: 
                - blue
      containers:
      - image: nginx
        name: nginx
        resources: {}

status: {}
```



8 / 8

Create a new deployment named `red` with the `nginx` image and `2` replicas, and ensure it gets placed on the `controlplane` node only.

Use the label key - `node-role.kubernetes.io/control-plane` - which is already set on the `controlplane` node.

Name: red

Replicas: 2

Image: nginx

NodeAffinity: requiredDuringSchedulingIgnoredDuringExecution

Key: node-role.kubernetes.io/control-plane

Use the right operator



```
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: red
  name: red
spec:
  replicas: 2
  selector:
    matchLabels:
      app: red
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: red
    spec:
      affinity:
        nodeAffinity: 
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: node-role.kubernetes.io/control-plane
                operator: Exists
      containers:
      - image: nginx
        name: nginx
        resources: {}

status: {}
```

