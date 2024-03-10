# Lab #8



3 / 12 Create a taint on `node01` with key of `spray`, value of `mortein` and effect of `NoSchedule`

```
k taint nodes node01 spray=mortein:NoSchedule
```

7 / 12 Create another pod named `bee` with the `nginx` image, which has a toleration set to the taint `mortein`.

```
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: bee
  name: bee
spec:
  containers:
  - image: nginx
    name: bee
    resources: {}
  dnsPolicy: ClusterFirst
  tolerations:
  - key: "spray"
    operator: "Equal"
    value: "mortein"
    effect: "NoSchedule"
  restartPolicy: Always
status: {}
```



10/12 remove a `Taint` from a node

```
controlplane ~ ➜  k taint nodes controlplane control-plane:NoSchedule-
node/controlplane untainted

controlplane ~ ➜  k taint nodes controlplane node-role.kubernetes.io/control-plane:NoSchedule-
node/controlplane untainted
```





