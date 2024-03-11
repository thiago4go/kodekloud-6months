# 🔀 Multi-Container Patterns

## Multi-Container Definitions

The idea of kubernetes is to run the application as microservices, usually with one pod per container, but some times we need to put more that one container, in this case the containers will share de volume and network within the Pod

## Sidecar

Most commom case:  Main App and Logger App

## Adaptor

Most commom case:  Main App and Logger App that adapt the log before sending to central server

## Embasador

This patter modify the connectivity so the Main Application do not need to care how it will connect to external services



## Init Containers

In a multi-container pod, each container is expected to run a process that stays alive as long as the Pod's lifecycle. For example in the mult-container pod that have a web application and a logging agente, both the containers are expected to stay alive att all times. The process running in the log agent container is expected to stay alive as long as the web application is running. If any of them fails, the Pod Restarts!

But at times we may want to run a process to completion in a container. For example a process that pulls a code or binary from a repository that will be used by the main application. That is the tast that will run only one time when the pod is first created. Or a process that waits for an external service or database to be up defore the actual application starts. That where initContainers comes in!.



An **initContainer** is configured in a pod like all other containers, except that it is specified inside an `initContaiers` section, like this:

{% code overflow="wrap" %}
```
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox:1.28
    command: ['sh', '-c', 'echo The app is running! && sleep 3600']
  initContainers:
  - name: init-myservice
    image: busybox
    command: ['sh', '-c', 'git clone <some-repository-that-will-be-used-by-application> ;']
```
{% endcode %}



When a Pod is first created the initContainer runs, and the process within it must run to a completion before the real container hosting the application starts.

We can configure multiple such  `initContainers` as well, like how we didi for multi-pod containers. In that case each init container runs **one at a time in sequential order.**

If any of the initContainers fails to complete, Kubernetes restrart the pod repeatedly until the initContainer succeeds.\


## Ephemeral Containers

We may use ephemeral containers to inspect services rather than to build applications.

Pods are the fundamental building block of k8s applications.   Sometimes it's necessary to inspect the sate off an existing Pod, however, for example to troubleshooot a hard-to-reproduce bug. In these cases you can run an ephemeral container in a existing Pod to inspect its state and run arbitrary commnadns.

Ephemeral containers are created using a special `ephemeralcontainers` handler in the API rather than by adding them directly to `pod.spec`, so it's not possible to add an ephemeral container using `kubectl edit`.

Ephemeral containers are useful for interactive troubleshooting when `kubectl exec` is insufficient because a container has crashed or a container image doesn't include debugging utilities.

> **Note:** Ephemeral containers are not supported by [static pods](https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/).



