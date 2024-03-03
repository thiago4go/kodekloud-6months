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



{% hint style="info" %}
export do='—dry-run=client -o yaml'

then use $do to create a YAML file&#x20;

\
alias kns=“kubectl config set-context —curent —namespace “\
\
kubectl explain \<resource>.\[path] --recursive | less

kubectl explain pod.spec --recursive | less

kubectl explain pod.spec.containers --recursive | less

kubectl explain pod.spec.volumes --recursive | less
{% endhint %}

{% hint style="info" %}
3\. Bookmark/Open [https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands) on the exam browser as soon as you log in. This would be helpful if you forget any kubectl commands

4\. The exam uses multiple kubernetes context. Be sure to run the commands on the correct context.

5\. While modifying any file, make a copy beforehand

6\. Learn docker commands (build, tag, save, inspect) as well.
{% endhint %}

{% hint style="info" %}


speed:

* I only used two alias for --dry-run=client -o yaml one for k describe, I should had one for k apply -f aswell since it seems to needed more than I initially thought.
* In the actual test I had two terminals open. On the right side of the screen I had the "work" terminal where I do all the actual work and on the left I have the "doc" terminal which I used for k explain. I had the work on the right since having the terminal and the kubernetes docs made it easier to check since I could have them side by side.
* Basic vim things - like /, yy, 3yy, dd, ctrl-v and p helped me speedup a bit
* getting used to doing k -n \<namespace> saves a lot of time with autocomplete
* k -h for anything that you don't understand makes life so much easier. Was able to figure how to run a cronjob manually as a job using that.
* I did do a lot of things imperatively.\

{% endhint %}

{% hint style="info" %}
2\. The second option is to extract the pod definition in YAML format to a file using the command

`kubectl get pod webapp -o yaml > my-new-pod.yaml`


{% endhint %}
