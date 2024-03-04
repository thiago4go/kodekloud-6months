# Lab #2

{% code title="pod-description.yaml" %}
```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: "2024-03-04T08:11:23Z"
  labels:
    name: webapp-color
  name: webapp-color
  namespace: default
  resourceVersion: "799"
  uid: 51d3475b-4a98-473b-9543-522562f0988f
spec:
  containers:
  - env:
    - name: APP_COLOR
      value: pink
    image: kodekloud/webapp-color
    imagePullPolicy: Always
    name: webapp-color
    resources: {}
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
    volumeMounts:
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: kube-api-access-gxpd9
      readOnly: true
  dnsPolicy: ClusterFirst
  enableServiceLinks: true
  nodeName: controlplane
  preemptionPolicy: PreemptLowerPriority
  priority: 0
  restartPolicy: Always
  schedulerName: default-scheduler
  securityContext: {}
  serviceAccount: default
  serviceAccountName: default
  terminationGracePeriodSeconds: 30
  tolerations:
  - effect: NoExecute
    key: node.kubernetes.io/not-ready
    operator: Exists
    tolerationSeconds: 300
  - effect: NoExecute
    key: node.kubernetes.io/unreachable
    operator: Exists
    tolerationSeconds: 300
  volumes:
  - name: kube-api-access-gxpd9
    projected:
      defaultMode: 420
      sources:
      - serviceAccountToken:
          expirationSeconds: 3607
          path: token
      - configMap:
          items:
          - key: ca.crt
            path: ca.crt
          name: kube-root-ca.crt
      - downwardAPI:
          items:
          - fieldRef:
              apiVersion: v1
              fieldPath: metadata.namespace
            path: namespace
```
{% endcode %}

{% code title="webapp-color-service.yaml" %}
```yaml
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: "2024-03-04T08:11:23Z"
  name: webapp-color-service
  namespace: default
  resourceVersion: "791"
  uid: cf06b63e-4ec4-488b-a692-0663d9e65c59
spec:
  clusterIP: 10.43.43.99
  clusterIPs:
  - 10.43.43.99
  externalTrafficPolicy: Cluster
  internalTrafficPolicy: Cluster
  ipFamilies:
  - IPv4
  ipFamilyPolicy: SingleStack
  ports:
  - nodePort: 30080
    port: 8080
    protocol: TCP
    targetPort: 8080
  selector:
    name: webapp-color
  sessionAffinity: None
  type: NodePort
status:
  loadBalancer: {}
```
{% endcode %}

7/11 How many ConfigMaps are in the default namespace?

```
// Some code
k get configmaps
```

8/11 identify the database host from the config map `db-config`

```
k get configmaps db-config -o yaml
apiVersion: v1
data:
  DB_HOST: SQL01.example.com
  DB_NAME: SQL01
  DB_PORT: "3306"
kind: ConfigMap
metadata:
  creationTimestamp: "2024-03-04T08:21:33Z"
  name: db-config
  namespace: default
  resourceVersion: "1000"
  uid: a2a88d58-f2ea-4bca-986b-1f55c729a764
```

9/11 Create a new ConfigMap for the `webapp-color` POD. Use the spec given below.

ConfigMap Name: webapp-config-map

Data: APP\_COLOR=darkblue

Data: APP\_OTHER=disregard

```
// Some code
k create configmap webapp-config-map --dry-run=client -o yaml > webapp.yaml
vi webapp.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  creationTimestamp: null
  name: webapp-config-map
data:
  APP_COLOR: darkblue
  APP_OTHER: disregard

k apply -f webapp.yaml

```

```
// Some code
k create cm webapp-config-map --from-literal=APP_COLOR=darkblue
```

10/11 Update the environment variable on the POD to use only the APP\_COLOR key from the newly created ConfigMap.

Note: Delete and recreate the POD. Only make the necessary changes. Do not modify the name of the Pod.

```
// Some code
k explain pod.spec.containers
k explain pod.spec.containers.env.valueFrom
```

```
// Some code

  - env:
    - name: APP_COLOR
      valueFrom:
        configMapKeyRef:
          name: webapp-config-map
          key: APP_COLOR
```

