# 👮 Security

## Authentication, Authorization and Admission Control

Users: Admins, Developers, Bots, Human and Robots

Kube-apiserver: Auth Mechanism using AccountServices

{% hint style="info" %}
## Important Updates

Before moving to the “KubeConfig” lecture I would like to share some updates: –

How to generate certificates for different Kubernetes components and for a user and use them in the Kubernetes cluster is not in the scope of the official CKAD exam.

These are part of the official CKA exam.
{% endhint %}

## KubeConfig

```
kubect get pod --kubeconfig config
```

it is a file tha can store kubernetes configuration, usually located in `$HOME/.kube/config`

This file have the following format:

<figure><img src="../.gitbook/assets/image (2) (1) (1).png" alt=""><figcaption></figcaption></figure>

`current-context` can be set as well

It links the clusters with users via contexts

```
kubectl config view
```

Also is possible to change other `configs` using the imperative mode

To append a new config file

```
export KUBECONFIG="${KUBECONFIG}:${HOME}/my-kube-config"
```

## API Groups

We always use API to connect to Kubernetes#

{% tabs %}
{% tab title="Kubernetes API" %}
```ruby
#core
/api
/api/v1/
/api/v1/namespaces
/api/v1/pods
/api/v1/rc
/api/v1/events
/api/v1/endpoints
/api/v1/nodes
/api/v1/bindings
/api/v1/PV
/api/v1/PVC
/api/v1/configmaps
/api/v1/secrets
/api/v1/services
#named
/apis
/apis/apps
/apis/extensions
/apis/networking.k8s.io
/apis/storage.k8s.io
/apis/authentication.k8s.io
/apis/certificates.k8s.io
```
{% endtab %}
{% endtabs %}

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

Use kubectl proxy to access the API endpoint without need to pass credentials parameters everytime

```
kubectl proxy

curl http://localhost:8001 -k
```

{% hint style="info" %}
Every API have Resouces and Verbs, them we can use this to allow or deny access to users.
{% endhint %}

## Authorization

Set the least privilage to the user and services

### Node Authorizer

A node using the Kube API to communicate to Kubelet is certify by `system:node:node#`

### ABAC (Attribute-based access control)

Set permissons for user and group, it need to be set manually and restart the KUBE API Server

{% code overflow="wrap" %}
```json
{"kind": "Policy", 
"spec": { 
"user":"dev-user",
"namespace":"*",
"resource":"pods",
"apiGroup":"*" }
}
```
{% endcode %}

### RBAC (Role-based access control)

<figure><img src="../.gitbook/assets/image (1) (1).png" alt=""><figcaption></figcaption></figure>

Role object\


<figure><img src="../.gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>

{% code title="developer-role.yaml" %}
```
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
rules:
- apiGroups:[""]
  resources: ["podes"]
  verbs: ["list","get","create","update","delete"]
  resourcesNames: ["blue", "red"]
- apiGroups: [""]
  resources: ["ConfigMap"]
  verbs: ["create"]
  
```
{% endcode %}

```
apiVersion: rbca.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: devuser-developer-binding
subjects:
- kind: User
  name: dev-user
  apiGroup: rbac.authorizartion.k8s.io
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io
```

> when creating remember to set the namespace, otherwise it will be on the defaulta namespace

As an User you can check access using:\


```
kubectl auth can-i <command> <resource> --as <user> --ns <namespace>
```

### Webhook

It is a thirdy part access control



### Authorization Mode

it follow the order specify in this line, also have the `AlwaysAllow` and `AlwaysDeny`

<div align="left">

<figure><img src="../.gitbook/assets/image (2) (1).png" alt=""><figcaption></figcaption></figure>

</div>

### Cluster Roles

Cluster Roles are made to control everything not under `namespaces`

```
k  api-resources --namespaced=false
```

To authorize in a cluster we can create `ClusterRole` and `ClusterRoleBinding`

It also can be used to give wider access to spacenamed resources on the cluster



## Admission Controllers

View Enabled Admission Controllers

{% code overflow="wrap" %}
```
kubect exec kube-apiserver-controlplane -n kube-system -- kube-apiserver -h | grep enable-admission-lugins
```
{% endcode %}

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Note that the `NamespaceExists` and `NamespaceAutoProvision` admission controllers are deprecated and now replaced by `NamespaceLifecycle` admission controller.

The `NamespaceLifecycle` admission controller will make sure that requests\
to a non-existent namespace is rejected and that the default namespaces such as\
`default`, `kube-system` and `kube-public` cannot be deleted.
{% endhint %}

### Validating and Mutating Admission Controllers

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

It is possible to also create a Admission Webhook Service for admission controler that will mutante or/and validade the request.

To deploy as pod inside the kubernete cluster and then create a `service`&#x20;

```
apiVersion: admissionregistration.k8s.io/v1
kind: mutatingwebhookconfigurations
metadata:
  name: "pod-policy.example.com"
webhooks:

```

<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>



## API Versions

* v1 - means GA version
* vXbetaY - may become GA in the future

You can set the version you want to use as PreferredVersion and also the Storage version

Also alpha version is not enable as default



### API Deprecations

rule #1: API elements may only be removed by incrementng the version of the API group

rule #2: API objects must be able to round-trip between API versions in a given release without information loss, with the exception of whole REST resources that do not exist in some versions.

rule #3:  About support older versions:

* GA: 12 months or 3 releases (whichever is longer)
* Beta: 9 months or 3 releases(whichever is longer)
* Alpha: 0 releases

Releases notes must indicate how to update



### Kubectl Convert

This help to convert between versions of the API

This command is not avaible as default, it needed to be installed



## Custom Resource Definition

apiextensions.k8s.io/v1

CustomResourceDefinition

#### Custom Controllers

Build it using Go or other laguage, based on the Sample-Controller, them contenarize it and run as a pod.



#### Operator Framework

This can joint CRD and CController and also much more!





