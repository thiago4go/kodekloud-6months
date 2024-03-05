# Lab #5

1/6What is the user used to execute the sleep process within the `ubuntu-sleeper` pod?

```
// Some code
kubectl exec ubuntu-sleeper -- ps aux | grep sleep
```

{% hint style="info" %}
it is possible to open bahs as well\
kubectl exec -it ubuntu-sleeper -- /bin/bash

id
{% endhint %}

2/6 Edit the pod `ubuntu-sleeper` to run the sleep process with user ID `1010`.&#x20;

```
// Some code
controlplane ~ ➜  k edit pod
error: pods "ubuntu-sleeper" is invalid
A copy of your changes has been stored to "/tmp/kubectl-edit-2287593878.yaml"
error: Edit cancelled, no valid changes were saved.

controlplane ~ ✖ k delete pod ubuntu-sleeper 
pod "ubuntu-sleeper" deleted

controlplane ~ ➜  k apply -f /tmp/kubectl-edit-2287593878.yaml
pod/ubuntu-sleeper created

controlplane ~ ➜  

    securityContext:
      runAsUser: 1010
```

3/6  A Pod definition file named `multi-pod.yaml` is given. With what user are the processes in the `web` container started?

The pod is created with multiple containers and security contexts defined at the `Pod` and `Container` level.

```
// Some code
controlplane ~ ➜  cat multi-pod.yaml 
apiVersion: v1
kind: Pod
metadata:
  name: multi-pod
spec:
  securityContext:
    runAsUser: 1001
  containers:
  -  image: ubuntu
     name: web
     command: ["sleep", "5000"]
     securityContext:
      runAsUser: 1002

  -  image: ubuntu
     name: sidecar
     command: ["sleep", "5000"]

```
