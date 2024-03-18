# 💾 State Persistence

Storage in Docker (Containers)

FS:

/var/lib/docker\
&#x20;\|- aufs\
&#x20;\|- containers\
&#x20;\|- image\
&#x20;\|- volumes



create a volume in docker, this will associate and persist the volumes. Even if when the container is terminated the data is saved on the host

```
docker volume create data_volume
docker run -mount type=bind, source=/data_volume,target=/var/lib/mysql mysql
```

> Storage Drivers are resposible to manager the storage
>
> Volume Drivers are the reposible for the volumes and depends on the Storage Data



## Volumes

We can associate a volume and then mount it on the pod.



```
...pod definintion
spec:
  containers:
    volumeMounts:
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: kube-api-access-fz5qk
      readOnly: true
    - mountPath: /log
      name: webapp
  volumes:
  - name: webapp
    hostPath: 
      path: /var/log/webapp
```



## Persistent Volume

{% code title="pv-definition.yaml" %}
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-log
spec:
  capacity:
    storage: 100Mi
  accessModes:
    - ReadWriteMany
  hostPath:
    path: /pv/log
  persistentVolumeReclaimPolicy: Retain
        
```
{% endcode %}

```
k create -f pv-definition.yaml
```

```
k get persistentvolumes
```

### Persistent Volume Claims

The admin create the PV and the user create PVC

The binding happens following the parameters like, Sufficient Capacity, Access Modes, Volume Modes, Storage Class and Selectors.

Once binded the PV cannot me used by other workload, and when the Pod stops the Volume Persist, we can change the&#x20;

{% code title="pvc-definition.yaml" %}
```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
      
```
{% endcode %}

```
k create -f pvc-definition.yaml
```

```
k get pvc
```

### Using PVCs in Pods

Once you create a PVC use it in a POD definition file by specifying the PVC Claim name under persistentVolumeClaim section in the volumes section like this:

```
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
    - name: myfrontend
      image: nginx
      volumeMounts:
      - mountPath: "/var/www/html"
        name: mypd
  volumes:
    - name: mypd
      persistentVolumeClaim:
        claimName: myclaim
```

<figure><img src="../../.gitbook/assets/image (14).png" alt=""><figcaption></figcaption></figure>
