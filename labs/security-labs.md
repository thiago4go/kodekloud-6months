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



Create a `ClusterRole` to give access to Nodes and Bind it to a `User`

```
controlplane ~ ➜  cat nodes.yaml 
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: nodes-access
rules:
- apiGroups:
  - ''
  resources:
  - 'nodes'
  verbs:
  - '*'

controlplane ~ ➜  cat bind.yaml 
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: node-access-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: nodes-access 
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: michelle

```



Create new access to StorageClass and PersistentVolumes, get the apiversion from&#x20;

```
kubectl api-resources
```

\


```
controlplane ~ ➜  cat storage.yaml 
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: storage-admin
rules:
- apiGroups:
  - 'storage.k8s.io/v1'
  resources:
  - 'storageclasses'
  - 'persistentvolumes'
  verbs:
  - '*'
  
  controlplane ~ ➜  cat sbind.yaml 
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: michelle-storage-admin
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: storage-admin 
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: michelle
```





Disable `DefaultStorageClass` admission controller

This admission controller observes creation of `PersistentVolumeClaim` objects that do not request any specific storage class and automatically adds a default storage class to them. This way, users that do not request any special storage class do not need to care about them at all and they will get the default one.

_Note:_ Once you update `kube-apiserver yaml` file then please wait few mins for the `kube-apiserver` to restart completely.



```
vi /etc/kubernetes/manifests/kube-apiserver

    - --enable-admission-plugins=NodeRestriction,NamespaceAutoProvision
```



Since the `kube-apiserver` is running as pod you can check the process to see enabled and disabled plugins.

```
ps -ef | grep kube-apiserver | grep admission-plugins
```



4 / 13

Create TLS secret `webhook-server-tls` for secure webhook communication in `webhook-demo` namespace.

We have already created below cert and key for webhook server which should be used to create secret.

Certificate : `/root/keys/webhook-server-tls.crt`

Key : `/root/keys/webhook-server-tls.key`

{% code overflow="wrap" %}
```

controlplane ~ ➜  k -n webhook-demo create secret tls webhook-server-tls --cert=/root/keys/webhook-server-tls.crt --key=/root/keys/webhook-server-tls.key
```
{% endcode %}

{% tabs %}
{% tab title="pod-with-defaults" %}
```javascript
# A pod with no securityContext specified.
# Without the webhook, it would run as user root (0). The webhook mutates it
# to run as the non-root user with uid 1234.
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-defaults
  labels:
    app: pod-with-defaults
spec:
  restartPolicy: OnFailure
  containers:
    - name: busybox
      image: busybox
      command: ["sh", "-c", "echo I am running as user $(id -u)"]
```
{% endtab %}

{% tab title="pod-with-override" %}
```python
# A pod with a securityContext explicitly allowing it to run as root.
# The effect of deploying this with and without the webhook is the same. The
# explicit setting however prevents the webhook from applying more secure
# defaults.
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-override
  labels:
    app: pod-with-override
spec:
  restartPolicy: OnFailure
  securityContext:
    runAsNonRoot: false
  containers:
    - name: busybox
      image: busybox
      command: ["sh", "-c", "echo I am running as user $(id -u)"]
```
{% endtab %}

{% tab title="pod-with-conflict" %}
```yaml

# A pod with a conflicting securityContext setting: it has to run as a non-root
# user, but we explicitly request a user id of 0 (root).
# Without the webhook, the pod could be created, but would be unable to launch
# due to an unenforceable security context leading to it being stuck in a
# 'CreateContainerConfigError' status. With the webhook, the creation of
# the pod is outright rejected.
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-conflict
  labels:
    app: pod-with-conflict
spec:
  restartPolicy: OnFailure
  securityContext:
    runAsNonRoot: true
    runAsUser: 0
  containers:
    - name: busybox
      image: busybox
      command: ["sh", "-c", "echo I am running as user $(id -u)"]

```
{% endtab %}

{% tab title="webhook-configuration" %}
```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: MutatingWebhookConfiguration
metadata:
  name: demo-webhook
webhooks:
  - name: webhook-server.webhook-demo.svc
    clientConfig:
      service:
        name: webhook-server
        namespace: webhook-demo
        path: "/mutate"
      caBundle: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURQekNDQWllZ0F3SUJBZ0lVZWxUakZmUW0wWmUrWFlUbHJTL20vSFlVSkxjd0RRWUpLb1pJaHZjTkFRRUwKQlFBd0x6RXRNQ3NHQTFVRUF3d2tRV1J0YVhOemFXOXVJRU52Ym5SeWIyeHNaWElnVjJWaWFHOXZheUJFWlcxdgpJRU5CTUI0WERUSTBNRE14T1RBNU16WTBNVm9YRFRJME1EUXhPREE1TXpZME1Wb3dMekV0TUNzR0ExVUVBd3drClFXUnRhWE56YVc5dUlFTnZiblJ5YjJ4c1pYSWdWMlZpYUc5dmF5QkVaVzF2SUVOQk1JSUJJakFOQmdrcWhraUcKOXcwQkFRRUZBQU9DQVE4QU1JSUJDZ0tDQVFFQXFPSWNML3JremViYVFYckR4UGd0ZW9VWW1tMEVYQlBBQ0RQaQpRZ2g2ZVU0ZjJNMklqc0RURCtYZVBaUU1JM0gvSElGNk5yalBIL1A2N28yUVNZbWt5QXZrc3ByK1pkekxTWGFvCmpQOEw2UVdOVjJLL0NVR0c4Y25ZSmNubitaeUJKdERrQ0cxOHgvaEwyQjIxT3ZDbHFPb29wdURsTlh3RXI3cHAKaHlISDFURUp3VnNsTE52YmxMRlVmUkd5czZMUVIyMVAxdHIrcnJrNlMwWUZCUU9xUFd3RTgxUUIyLzlKTEdHbgpZWEF2NjFCT1kwSDVPVlp6WnZXM1FFcFRBVWhnZDJ1SVU1dVo3cGJwNm5rdDJYTGZWcnRGSTNoZVBSTHg3NVZ1CmUrUnpXeWVSZW5OUWNrT1dOZjcwU1FzVWl1TjkxMzBRVHhSRFZQVzdxb1A1Q0x5aml3SURBUUFCbzFNd1VUQWQKQmdOVkhRNEVGZ1FVV3FLVGZCUzcxdkNoRDR3S1B4SkxBclNxYnhvd0h3WURWUjBqQkJnd0ZvQVVXcUtUZkJTNwoxdkNoRDR3S1B4SkxBclNxYnhvd0R3WURWUjBUQVFIL0JBVXdBd0VCL3pBTkJna3Foa2lHOXcwQkFRc0ZBQU9DCkFRRUFnMEhvNGJ5Y2hRNGMwRy9OZlZHM2N6M3VIOVcrN0xvYmpwbEFiR000V0tGUHhiUGhRaktYLzZJZ2JZZ3AKYkMzSm80UmY1WEkwZHNRS1RGWERHVkU0a24xK3JiQnd0SnR2ZzBITjdJWE51MFNKdXQ2TlhYK200SU16bEN5KwpNK25vSUY3cUZrNVo2YUVEdVlWTzByK1UzMzQrTW5SdktQS1BwRDJCOUtHUkZ1ZnRTYi9BS1Z0RU9Sc3Y3RWNJCm1UNEE4NlZndVhhUlNYc1FnN09pMkNLREkvNzlCSGlqbXNFUTRFWEdmNWVjN3VJUHVtV3pRZTE0K2E3SHUrWFYKSjJZRTJmV3ljOTB1NkZVUEE5SVJQenl3V1loKy9TNVhWdUFVbkcyZFltOVY5YjFzdThETWZjS3gxVE1zT29XbQptR2ZEaGxnZGFzbThRaFdjY0huVXdpUCtHdz09Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K
    rules:
      - operations: [ "CREATE" ]
        apiGroups: [""]
        apiVersions: ["v1"]
        resources: ["pods"]
    admissionReviewVersions: ["v1beta1"]
    sideEffects: None

```
{% endtab %}

{% tab title="webhook-service" %}
```
apiVersion: v1
kind: Service
metadata:
  name: webhook-server
  namespace: webhook-demo
spec:
  selector:
    app: webhook-server
  ports:
    - port: 443
      targetPort: webhook-api
```
{% endtab %}

{% tab title="webhook-deployment" %}
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webhook-server
  namespace: webhook-demo
  labels:
    app: webhook-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: webhook-server
  template:
    metadata:
      labels:
        app: webhook-server
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1234
      containers:
      - name: server
        image: stackrox/admission-controller-webhook-demo:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8443
          name: webhook-api
        volumeMounts:
        - name: webhook-tls-certs
          mountPath: /run/secrets/tls
          readOnly: true
      volumes:
      - name: webhook-tls-certs
        secret:
          secretName: webhook-server-tls
```
{% endtab %}
{% endtabs %}



In previous steps we have deployed demo webhook which does below

\- Denies all request for pod to run as root in container if no securityContext is provided.

\- If no value is set for runAsNonRoot, a default of `true` is applied, and the user ID defaults to `1234`

\- Allow to run containers as root if runAsNonRoot set explicitly to `false` in the securityContext

In next steps we have added some pod definitions file for each scenario. Deploy those pods with existing definitions file and validate the behaviour of our webhook



4/7 What is the preferred version for `authorization.k8s.io` api group?

```
kubectl proxy 8001&
curl localhost:8001/apis/authorization.k8s.io
```





## Custom Resource Definition

```
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: internals.datasets.kodekloud.com
spec:
  group: datasets.kodekloud.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                internalLoad:
                  type: string
                range:
                  type: integer
                percentage:
                  type: string
  scope: Namespaced
  names:
    plural: internals
    singular: internal
    kind: Internal
    shortNames:
    - int
```



```
apiVersion: datasets.kodekloud.com/v1
kind: Internal
metadata:
  name: internal-space
  namespace: default
spec:
  internalLoad: "high"
  range: 80
  percentage: "50"
```

