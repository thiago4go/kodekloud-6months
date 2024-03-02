# Lab #2

2/16 How many ReplicaSet exists?

```
// Some code
alias kgr='kubectl get replicasets'
kgr
```

3/16 How many Pods are `DESIRED` in the `new-replica-set`?

4/16 What image was used on the `new-replica-set` ?

```
// Some code
alias kdp='kubectl describe pod'
kdp new | grep Image
```

6/16 How many Pods are READY in the `new-replica-set`?

```
// Some code
kgr
```

10/16 Why there still 4 Pods, even after you deleted one?

{% hint style="info" %}
ReplicaSet ensures that desired number of Pods always runs
{% endhint %}

11/16 Create a ReplicaSet using the `replicaset-definition-1.yaml` file located at `/root/`

there is an issue witht he file, so try to fix it.

{% code overflow="wrap" %}
```bash
// Some code
controlplane ~ ➜  k apply -f replicaset-definition-1.yaml 
error: resource mapping not found for name: "replicaset-1" namespace: "" from "replicaset-definition-1.yaml": no matches for kind "ReplicaSet" in version "v1"
ensure CRDs are installed first
```
{% endcode %}

The problem is the apiVersion, replicaSet must use apps/v1

12/16 Fix the issue in the `replicaset-definition-2.yaml` file and creat a `ReplicaSet` using it/

{% code overflow="wrap" %}
```bash
// Some code
controlplane ~ ➜  k apply -f replicaset-definition-2.yaml 
The ReplicaSet "replicaset-2" is invalid: spec.template.metadata.labels: Invalid value: map[string]string{"tier":"nginx"}: `selector` does not match template `labels`
```
{% endcode %}

13/16 Delete the two newly created ReplicaSets - `replicaset-1` and `replicaset-2`

```
// Some code
k delete replicaset replicaset-1 replicaset-2
```

14/16 Fix the original replica set `new-replica-set` to use the correct `busybox` image.

{% hint style="info" %}
Either delete and recreate the ReplicaSet or Update the existing ReplicaSet and then delete all Pods, so new ones with the correct image will be created.
{% endhint %}

```
// Some code
k edit replicaset new-replica-set
k delete pod <pod1> <pod2> <pod3> <pod4>
```

15/16 Scale the ReplicaSet to 5 pods

Use `kubectl scale` command or edit the replicaset using `kubectl edit replicaset.`

```
// Some code
k scale --replicas=5 rs/new-replica-set
```

16/16 Now sacle the ReplicaSet down to 2 Pods.

Use `kubectl scale` command or edit the replicaset using `kubectl edit replicaset.`

```
// Some code
k edit rs new-replica-set
```
