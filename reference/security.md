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

it is a file tha can store kubernetes configuration, usually located in `$HOME/.kube/config`

This file have the following format:

<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

```
kubectl config view
```







