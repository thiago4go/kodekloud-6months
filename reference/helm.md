# ⚗️ Helm

Package Manager of Kubernetes

It helps to control every object in an application.



```
helm install <app>
helm upgrrade
helm rollback
helm uninstall
```

&#x20;

### Helm Concepts

templates + values = helm chart

searching for helm charts

```
helm search hub <appname>
```

also is possible to add repositories

```
helm repo add bitnami https://charts.bitnami.com/bitnami
```

```
helm search repo <app-name>
helm repo list
```

To install:

```
helm install <release-name> <app-name>
```



