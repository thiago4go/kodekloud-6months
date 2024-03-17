# ⚙️ Configurantion

## Enviroment Variables Concepts in Docker and K8S

Create a Docker Image

Commands and Arguments in Docker

`docker run <image>`

`docker run <image> <command> <parameter>`

{% hint style="info" %}
ENTRYPOINT is how the application starts
{% endhint %}

Commands and Arguments in K8S

<figure><img src="../.gitbook/assets/image (6) (1).png" alt=""><figcaption></figcaption></figure>

Enviroment Variable

<figure><img src="../.gitbook/assets/image (3) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

## ConfigMaps

```
// literal
k create configmap <config-name> --from-literal=<key>=<value>
// from file
k create configmap <config-name> --from-file=app.config.properties
```

declarative way

{% code title="config-map.yaml" %}
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_COLOR: blue
  APP_MODE: prod
```
{% endcode %}

```
k apply -f config-map.yaml
```

Inject ConfiMap Env Variable in a pod via `envFrom`

<figure><img src="../.gitbook/assets/image (4) (1) (1).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (5) (1) (1).png" alt=""><figcaption></figcaption></figure>

## Create Secrets

imperative way

using `--from-literal`

```
// Some code
kubectl create secret generic <secret-name> --from-literal=<key>=<value>
```

make a file as JSON `secret.properties`

```
// Some code
DB_HOST: mysql
DB_USER: root
DB_Password: paswrd
```

them use `--from-file`

```
// Some code
kubectl create secret generic <secret-name> --from-file=secret.properties
```

<figure><img src="../.gitbook/assets/image (8).png" alt=""><figcaption><p>Encode Scretes</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (1) (2).png" alt=""><figcaption><p>Decode Secrets</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (4) (1).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Secrets is not Encrypted! > use Encrypt at rest
{% endhint %}

<figure><img src="../.gitbook/assets/image (5) (1).png" alt=""><figcaption></figcaption></figure>

Secrets are not encrypted, so it is not safer in that sense. However, some best practices around using secrets make it safer. As in best practices like:

* Not checking-in secret object definition files to source code repositories.
* [Enabling Encryption at Rest ](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/)for Secrets so they are stored encrypted in ETCD.

Also the way kubernetes handles secrets. Such as:

* A secret is only sent to a node if a pod on that node requires it.
* Kubelet stores the secret into a tmpfs so that the secret is not written to disk storage.
* Once the Pod that depends on the secret is deleted, kubelet will delete its local copy of the secret data as well.

Read about the [protections ](https://kubernetes.io/docs/concepts/configuration/secret/#protections)and [risks](https://kubernetes.io/docs/concepts/configuration/secret/#risks) of using secrets [here](https://kubernetes.io/docs/concepts/configuration/secret/#risks)

Having said that, there are other better ways of handling sensitive data like passwords in Kubernetes, such as using tools like Helm Secrets, [HashiCorp Vault](https://www.vaultproject.io/).&#x20;



## Security Contexts

Docker runs using namespace as bounderies to set the context and user and its capabilities

The `root user` within the container has some restricitions put in place by docker.

A root user in the system is the user that can do many things

{% hint style="info" %}
Check all capabilities in usr/include/linux
{% endhint %}

Kubernetes Security

**`securityContext` as part of spec.**

It can be set in the Pod level or in a Container level, with `runAsUser`, this last can also add `capabilities: add: ["MAC_ADMIN"]`, but it is not possible to add capabilities in the Pod level.

### Encrypting Secret Data at Rest

use `etcdctl`

{% hint style="info" %}
:anger: use  `k get pods -n kube-system` to get pods on the control-plane :anger:&#x20;
{% endhint %}

{% hint style="info" %}
to check if options is enable on kube-api

ps -aux | grep kube-api | grep "option-name"
{% endhint %}

{% hint style="info" %}
in a kubeadm setuo

cat /etc/kubernetes/manifests/kube-apiserver.yaml
{% endhint %}

## Resouce Requirements

pod.spec.containers.resources.requests

{% hint style="info" %}
1G = 10^9

1M = 10^6

1K = 10^3\
\
1Gi = 2^30

1Mi = 2^20

1Ki = 2^10
{% endhint %}

On pod definintion

```
// Some code
resources:
  requests:
    memory: "1Gi"
    cpu: 1
  limits:
    memory: "2Gi"
    cpu:2
```

### Exceed Limits

What happens when a pod tries to exceed resources beyond its specified limit?

In case of CPU, the system throttles the CPU so taht it does not go beyond the specified limit.

However, this is not the case with memory. A container can use more memory resources than its limit. So if a pod tries to consume more memory than its limit constatly, the pod will be terminated OOM (Out of Memory)



Default Behavior is no limit, no request.

<figure><img src="../.gitbook/assets/image (1) (1).png" alt=""><figcaption><p>Alwsys best to set request on CPU, but no need to set Limit</p></figcaption></figure>

### Limit Range

LimitRange.spec.limits

{% tabs %}
{% tab title="limit-range-cpu" %}
```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: cpu-resource-constraint
spec:
  limits:
  - default:
      cpu: 500m
    defaultRequest:
      cpu: 500m
    max:
      cpu: "1"
    min:
      cpu: 100m
    type: Container

```
{% endtab %}

{% tab title="limit-range-memory" %}
```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: memory-resource-constraint
spec:
  limits:
  - default:
      cpu: 1Gi
    defaultRequest:
      cpu: 1Gi
    max:
      cpu: 1Gi
    min:
      cpu: 500Mi
    type: Container

```
{% endtab %}
{% endtabs %}

### Resource Quotas

This restrict the toal amount of resources that can be consumned by applications deplyod in a cluster.

```
apiVersion: v1
kind: ResourceQuota
metadata:
  name: my-resouce-qouta
spec:
  hard:
    requests.cpu: 4
    requests.memory: 4Gi
    limits.cpu: 10
    llimits.memory: 10Gi

```

## ServiceAccounts

UserAccount vs ServiceAccounts

| UserAccount    | ServiceAccount      |
| -------------- | ------------------- |
| Admin          | Prometheus          |
| Developer      | Jenkins             |
| Used by Humans | Used by Application |



```
k create serviceaccount <service-name>
k get serviceaccount
```

{% hint style="info" %}
It will generate a Token that will be autmatically create as a secret
{% endhint %}

```
k describe secret <token-name>
```

Then use this token to autenticate an API

Changes on the newers versions

A token now have a defined lifetime that is generated by token request API

from version 1.24 the token is not create automatically after creating a service account, and it will associate directly without a sercret.

```
k create serviceaccount <serviceaccount-name>
k create token <serviceaccount-name>
```

But if using an YAML

```
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
  name: mysecretname
  annotations:
    kubernetes.io/service-account.name: <serviceaccount-name>

```



## Taints & Tolerantions

Pod and Nod relationship

Taint is like a why to restrict a pod to be schedule on a node

But some pod could be Tolerant to some Taint

To put Taint in a node:

```
k taint nodes <node-name> key=value:taint-effect
```

| taint-effect     | result                                         |
| ---------------- | ---------------------------------------------- |
| NoSchedule       | Will not be schedule                           |
| PreferNoSchedule | May not schedule                               |
| NoExecute        | Do not execute a pod, even if it already exist |

<figure><img src="../.gitbook/assets/image (2) (1).png" alt=""><figcaption></figcaption></figure>

```
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
  - name: nginx-caontiner
    image: nginx
  tolerations:
  - key: "app"
    operator: ""Equal"
    value: "blue"
    effect: "NoSchedule"
```



## Node Selectors and Node Affinity

pod.spec.nodeSelector

```
 nodeSelector:
        testkey: testvalue
```

```
kubectl label nodes <node-name> <key>=<value>
```

This have some limitions, like no attributes like NOT or AND



pod.spec.affinity.nodeAffinity.requireDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms.matchExpressions

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (7).png" alt=""><figcaption></figcaption></figure>

