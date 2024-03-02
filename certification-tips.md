# 🪄 Certification Tips

`--dry-run -o yaml >  file.yaml`

### Service

#### ClusterIP

Create a Service named redis-service of type ClusterIP to exp\[ose pode reds on port 6379

`k expose pod redis --port=6379 --name redis-service --dry-run=client -o yaml`

{% hint style="info" %}
This will automatically use the pod's lables as selectors
{% endhint %}

`kubectl create service clusterip redis --tcp=6379:6379 --dry-run=client -o yaml > service-file.yaml`&#x20;

{% hint style="info" %}
CAUTION

This will not use the pod labes as sector, instead it will assume selectors as app=redis&#x20;
{% endhint %}

#### NodePort

Create a service named nginx of type NodePort to expose pod nginx por 80 on port 30080 on the nodes:

`kubectl expose pod nginx --port=80 --name ngnix-service --type=NodePort --dry-run=client -o yaml > service-file.yaml`

{% hint style="info" %}
CAUTION

This will automactically use the pod's labels as selector, but you cannot specify the node port as option. Edit it on the file
{% endhint %}

or

`kubectl create service noteport nginx --tcp=80:80 -- node-port=30080 --dry-run=client -o yaml > service-file.yaml`

{% hint style="info" %}
CAUTION

This will not use pods labels as sectors. edit it on the file
{% endhint %}

> Both the above commands have their own challenges. While one of it cannot accept a selector the other cannot accept a node port. I would recommend going with the `kubectl expose` command. If you need to specify a node port, generate a definition file using the same command and manually input the nodeport before creating the service.

**Formatting Output with kubectl**

**`kubectl [command] [TYPE] [NAME] -o <output_format>`**

1. \-o json
2. \-o name \[Print only the resource name and nothing else]
3. \-o wide \[Output with wid - addition details]
4. \-o yaml
