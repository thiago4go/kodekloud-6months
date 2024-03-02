# 🗃️ Edit Pods

A note on editing existing pods

{% hint style="info" %}
If you are given a pod definition file, edit that file and use it to create a new pod

If you are not given a pod definition file, you may extract the definition to a file using the beflow command:
{% endhint %}

```
// Some code
kubectl get pod <pode-name> -o yaml > pod-definition.yaml
```

*   To modifiy the properties of the pod, you can utilize `kubectl edit pod <pod-name>` command. Please note that only properties listed below are editable:

    * `spec.containers[*].image`
    * `spec.initContainers[*].image`
    * `spec.activeDeadlineSecounds`
    * `spec.tolerantions`
    * `spec.terminationGracePeriodSeconds`


*
