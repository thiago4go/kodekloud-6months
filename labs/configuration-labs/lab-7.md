# Lab #7

1/14 how many `ServiceAccounts` are there in the default namespace?

```
k get serviceaccounts
```

&#x20;

2 / 14 What is the secret token used by the default service account?

```
k describe sa default
```

3 / 14 We just deployed the Dashboard application. Inspect the deployment. What is the image used by the deployment?

```
k describe deployment <deployment-name> | grep Image
```

10 / 14 The application needs a ServiceAccount with the Right permissions to be created to authenticate to Kubernetes. The default ServiceAccount has limited access. Create a new ServiceAccount named dashboard-sa.

```
k create sa dashboard-sa
```



13 / 14

You shouldn't have to copy and paste the token each time. The Dashboard application is programmed to read token from the secret mount location. However currently, the `default` service account is mounted. Update the deployment to use the newly created ServiceAccount

Edit the deployment to change ServiceAccount from `default` to `dashboard-sa`.



```
k explain deployment.spec.template.spec.serviceAccountName
```







