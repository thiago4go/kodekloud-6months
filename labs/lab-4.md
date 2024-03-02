# Lab #4

1/7 How many Namespaces exist on the system?

```
// Some code
k get namespaces
k get ns
```

2/7 How many pods are on `marketing` namespace?

```
// Some code
k get pods --namespace=marketing
k get pods -n=marketing
```

3/7 Create a PO in the finance namespace, use the spec five below:

name: redis

image name : redis

```
// Some code
k run redis --image=redis --namespace=finance
```

4/7 Which namespace has the `blue` pod in it?

```
// Some code
k get pods --all-namespaces | grep blue
k get pods -A | grep blue
```

7/7 What DNS name should `Blue` application use to access the database `db-service` in the `dev` namespace?

```
// Some code
db-service.dev.svc.cluster.local
```
