# Volumes Lab

```
apiVersion:  v1
kind: PersistentVolume
metadata:
  name: pv-log
spec:
  accessModes:
    - ReadWriteMany
  capacity:
    storage: 100Mi
  hostPath:
    path: /pv/log
  persistentVolumeReclaimPolicy: Retain  

```



```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: claim-log-1
spec:
  resources:
    requests:
      storage: 50Mi
  accessModes:
    - ReadWriteOnce
```

### &#x20;<a href="#claims-as-volumes" id="claims-as-volumes"></a>



