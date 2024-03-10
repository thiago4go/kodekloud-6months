# Lab #3

1/8 How many secrets are in the default namespace

```
// Some code
k get secrets
```

3/8 What is the type of the `dashboard-token` secret?

```
// Some code
k describe secrets dashboard-token
```

5/8

We are going to deploy an application with the below architecture

We have already deployed the required pods and services. Check out the pods and services created. Check out the web application using the `Webapp MySQL` link above your terminal, next to the Quiz Portal Link.

<figure><img src="../../.gitbook/assets/image (7) (1).png" alt=""><figcaption><p>app with secret architecture</p></figcaption></figure>

6/8 Create a new secret named `db-secret` with the data given below.

Secret Name: db-secret

Secret 1: DB\_Host=sql01

Secret 2: DB\_User=root

Secret 3: DB\_Password=password123

{% code overflow="wrap" %}
```
// Some code

k create secret generic  db-secret --from-literal=DB_Host=sql01 --from-literal=DB_User=root --from
-literal=DB_Password=password123
```
{% endcode %}

7/8 Configure `webapp-pod` to load environment variables from the newly created secret.

Pod name: webapp-pod

Image name: kodekloud/simple-webapp-mysql

Env From: Secret=db-secret

```
// Some code
k get pod webapp-pod -o yaml > pod.yaml

vi pod.yaml


```

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: "2024-03-04T10:00:14Z"
  labels:
    name: webapp-pod
  name: webapp-pod
  namespace: default
  resourceVersion: "839"
  uid: 89449348-fcd6-4741-9837-095f36067067
spec:
  containers:
  - image: kodekloud/simple-webapp-mysql
    imagePullPolicy: Always
    name: webapp
    resources: {}
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
    volumeMounts:
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: kube-api-access-f9jwn
      readOnly: true
    envFrom:
      - secretRef:
          name: db-secret
```

```
// Some code
k delete pod webapp-pod
k apply -f pod.yaml
```
