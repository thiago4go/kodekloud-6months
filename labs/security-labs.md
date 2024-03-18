# Security Labs

12/13  I would like to use the `dev-user` to access `test-cluster-1.` Set the current context to the right one so I can do that. Once the right context is identified, use the `kubectl config use-context` command.



{% code overflow="wrap" %}
```
kubectl config use-context research --kubeconfig /root/my-kube-config

```
{% endcode %}



Create a Role and Bind it to a User

```
controlplane ~ ➜  cat dev-user.yaml 
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer 
rules:
- apiGroups:
  - ""
  resources:
  - pods
  verbs: ["create","list","delete"]

controlplane ~ ➜  cat bind.yaml 
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-user-binding 
subjects:
- kind: User
  name: dev-user
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io

```





```
controlplane ~ ➜  k get roles -o yaml
apiVersion: v1
items:
- apiVersion: rbac.authorization.k8s.io/v1
  kind: Role
  metadata:
    creationTimestamp: "2024-03-18T11:09:46Z"
    name: developer
    namespace: blue
    resourceVersion: "742"
    uid: 0ce3ecd4-c702-4973-8a36-920b0c5dfd09
  rules:
  - apiGroups:
    - ""
    resourceNames:
    - blue-app
    resources:
    - pods
    verbs:
    - get
    - watch
    - create
    - delete
kind: List
metadata:
  resourceVersion: ""
```
