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

<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

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
