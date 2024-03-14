# 🔭 Observability

## Readiness Probes

Pod lifecycle, pod status - peding while not find a pod -> containercreating -> Running

Pod Conditions:

* PodScheduled
* Initialized
* ContainersReady
* Ready

```
kubectl describe pod
Conditions section
```

Kubernetes consider that a container created and running as READY, even if the application itself is not Ready yet.  Like Web application can be tested with HTTP test - /api/ready&#x20;

As a developer, we know better what means the application is ready

In a case of a WebServer or API

```
containers:
  readinessProbe:
    httpGet:
      path: /api/ready
      port: 8080
```

In a case of a database, test a Port / Socket

```
readinessProbe:
  tcpSocket:
     port: 3306
```

Or just execute some command or script

```
readinessProbe:
  exec:
    command: ["cat", "/api/is_ready"]
```

Also can use some wait period

```
readinessProbe:
  httpGet:
    path: /api/ready
    port: 8080
  initialDelaySeconds: 20
  periodSeconds: 5
  #default is 3 attemps
  failureThreshold: 8 
```

Also it is fundamental in a multpods, it is important to check if the container is really ready, since the networking service will make it available once its status is Ready



## Liveness Probe

Similar to readiness, Liveness is a healthy check on the application, and if it fails the pod will be deleted and restarted.

n a case of a WebServer or API

```
containers:
  livenessProbe:
    httpGet:
      path: /api/ready
      port: 8080
```

In a case of a database, test a Port / Socket

```
livenessProbe:
  tcpSocket:
     port: 3306
```

Or just execute some command or script

```
livenessProbe:
  exec:
    command: ["cat", "/api/is_ready"]
```

Also can use some wait period

```
livenessProbe:
  httpGet:
    path: /api/ready
    port: 8080
  initialDelaySeconds: 20
  periodSeconds: 5
  #default is 3 attemps
  failureThreshold: 8 
```

## Logging

{% code title="event-simulator.yaml" %}
```
apiVersion: v1
kind: Pod
metadata:
  name: event-simulator-pod
spec:
  containers:
  - name: event-simulator
    image: kodekloud/event-simulator
```
{% endcode %}

To check the log in a pod use this, also do not forget to use the container name if more tha one inside the pod

```
k logs -f event-simulator-pod event-simulator
```

















