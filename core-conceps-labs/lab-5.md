# Lab #5

2/9 Deploy a pod name nginx-pod using the nginx:alpine image

Use imperative commands only

```
// Some code
k run nginx-pod --image=nginx:alpine
```

3/9 Deploy a `redis` pod using the `redis:alpine` image with the labels set to `tier=db`

```
// Some code
k run redis --image=redis:alpine --labels tier=db
```

4/9 Create a service `redis-service` to expose the `redis` application within the cluster on port `6379`

```
// Some code
k expose pod redis --port=6379 --name redis-service
```

5/9 Create a deployment named `webapp` using the image `kodekloud/webapp-color` with `3` replicas

```
// Some code
k create deployment webapp --image=kodekloud/webapp-color --replicas=3
```

6/9 Create a new pod called `custom-nginx` using `nginx` image and expose it on `container port 8080`

```
// Some code
k run custom-nginx --image=nginx --port=8080
```

7/9 Create a new namespace called `dev-ns`

```
// Some code
k create ns dev-ns
```

8/9 Create a new deployment called `redis-deploy` in the `dev-ns` namespace with the `redis` image. It should have `2` replicas.

```
// Some code
k create deployment redis-deploy -n=dev-ns --image=redis -replicas=2 
```

9/9 Create a pod called `httpd` using the image `httpd:alpine` in the default namespace. Next, create a service of type `ClusterIP` by the same name `(httpd)`. The target port for the service should be `80`.

```
// Some code
k run httpd --image=httpd:alpine --expose --port=80
```
