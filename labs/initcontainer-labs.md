# InitContainer Labs

4 / 9 We have deployed an application logging stack in the `elastic-stack` namespace. Inspect it.

Before proceeding with the next set of questions, please wait for all the pods in the `elastic-stack` namespace to be ready. This can take a few minutes



There shouldn't be any logs for now.

We will configure a sidecar container for the application to send logs to Elastic Search.\
The application outputs logs to the file /log/app.log. View the logs and try to identify the user having issues with Login.

```

k -n elastic-stack exec -it app -- cat /log/app.log  
```

8 / 9

Edit the pod in the `elastic-stack` namespace to add a sidecar container to send logs to Elastic Search. Mount the log volume to the sidecar container.

Only add a new container. Do not modify anything else. Use the spec provided below.

> Note: State persistence concepts are discussed in detail later in this course. For now please make use of the below documentation link for updating the concerning pod.

\
`https://kubernetes.io/docs/tasks/access-application-cluster/communicate-containers-same-pod-shared-volume/`

Name: app

Container Name: sidecar

Container Image: kodekloud/filebeat-configured

Volume Mount: log-volume

Mount Path: /var/log/event-simulator/

Existing Container Name: app

Existing Container Image: kodekloud/event-simulator

<figure><img src="../.gitbook/assets/image (9).png" alt=""><figcaption></figcaption></figure>

```
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: "2024-03-11T06:15:52Z"
  labels:
    name: app
  name: app
  namespace: elastic-stack 
  resourceVersion: "931"
  uid: 3a19c167-a91f-46b1-988e-8ff76b8cab03
spec:
  containers:
  - image: kodekloud/event-simulator
    imagePullPolicy: Always
    name: app
    resources: {}
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
    volumeMounts:
    - mountPath: /log
      name: log-volume
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: kube-api-access-6ckms
      readOnly: true
  - image: kodekloud/filebeat-configured
    imagePullPolicy: Always
    name: sidecar
    resources: {}
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
    volumeMounts:
    - mountPath: /var/log/event-simulator/
      name: log-volume
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
  - hostPath:
      path: /var/log/webapp
      type: DirectoryOrCreate
    name: log-volume
  - name: kube-api-access-6ckms
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

```
k edit pod app -n elastic-stack
k replace --force -f /tmp/kubectl-edit-123123.yaml
```



8 / 9 Update the pod red to use an initContainer that uses the busybox image and sleeps for 20 seconds

Delete and re-create the pod if necessary. But make sure no other configurations change.

Pod: red

initContainer Configured Correctly

pod.spec.initContainers

```

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: "2024-03-11T07:55:50Z"
  name: red
  namespace: default
  resourceVersion: "814"
  uid: 82141567-edd5-4207-b9c7-5e1b29320700
spec:
  containers:
  - command:
    - sh
    - -c
    - echo The app is running! && sleep 3600
    image: busybox:1.28
    imagePullPolicy: IfNotPresent
    name: red-container
    resources: {}
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
    volumeMounts:
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: kube-api-access-gjs2k
      readOnly: true
  initContainers: 
  - command: 
    - sh 
    - -c 
    - sleep 20
    image: busybox 
    imagePullPolicy: Always 
    name: init-myservice 
    resources: {} 
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
  - name: kube-api-access-gjs2k
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

9 / 9 A new application orange is deployed. There is something wrong with it. Identify and fix the issue.

Once fixed, wait for the application to run before checking solution.



