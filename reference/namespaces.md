# 🌴 Namespaces

Default is the Default namespace

kube-system

kube-public



Create a new namespace is good for separete resources

It share the network as well, if it is in another namespace you may need to give the correct address



<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

```
// Some code
kubectl get pods --namespace=kube-system

kubectl create namespace <name>
```

{% hint style="info" %}
To switch the default namespace context

kubectl config set-context $(kubectl config current-context) --nemespace=\<name>
{% endhint %}

{% hint style="info" %}
To check resources in all namespaces

kubectl get all --all-namespaces
{% endhint %}

Reource Quota for Namespace

<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>
