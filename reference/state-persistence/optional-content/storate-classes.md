# Storate Classes

## Static vs Dynamic Provisioning

Using storage provisionners

```
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: google-storage
provisioner: kubernetes.io/gce-pd
```



<figure><img src="../../../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>
