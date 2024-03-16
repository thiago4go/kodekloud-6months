# Lab #3

Get all information from the cluster

```
k get all
```

7/11 What image was used on the ReplicaSet?

```
// Some code
k describe rs <replicaset-name> | grep Image
```



10/11 Create a new Deployment using the `deployment-definition-1.yaml` file locate at `/root/`

There is an issue with the file, so try to fix it

{% code overflow="wrap" %}
```bash
// Some code
controlplane ~ ➜  k apply -f deployment-definition-1.yaml 
Error from server (BadRequest): error when creating "deployment-definition-1.yaml": deployment in version "v1" cannot be handled as a Deployment: no kind "deployment" is registered for version "apps/v1" in scheme "k8s.io/apimachinery@v1.29.0-k3s1/pkg/runtime/scheme.go:100"
```
{% endcode %}

```
// Some code
vi <deployment.yaml>
```

This error is because deployment should be `kind: Deployment` with capital D

11/11 Create a new Deployment with the below attributes using your own deplyment definition file

Name: httpd-frontend

Replicas: 3

Image: httpd:2.4-alpine

{% code overflow="wrap" %}
```bash
// Some code
k create deployment httpd-fronted --image=httpd:2.4-alpine --replicas=3 --dry-run=client -o yaml > frontend-deployment.yaml
```
{% endcode %}

{% hint style="info" %}
Check the file using cat
{% endhint %}
