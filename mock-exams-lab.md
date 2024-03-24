# Mock Exams Lab

Task Create a cronjob called dice that runs every one minute. Use the Pod template located at /root/throw-a-dice. The image throw-dice randomly returns a value between 1 and 6. The result of 6 is considered success and all others are failure.

The job should be non-parallel and complete the task once. Use a backoffLimit of 25.

If the task is not completed within 20 seconds the job should fail and pods should be terminated.

You don't have to wait for the job completion. As long as the cronjob has been created as per the requirements.

apiVersion: batch/v1 kind: CronJob metadata: name: dice spec: schedule: "\*/1 \* \* \* \*" jobTemplate: spec: completions: 1 backoffLimit: 25 # This is so the job does not quit before it succeeds. activeDeadlineSeconds: 20 template: spec: containers: - name: dice image: kodekloud/throw-dice restartPolicy: Never

my version apiVersion: batch/v1 kind: CronJob metadata: name: hello spec: schedule: "\*/1 \* \* \* \*" jobTemplate: spec: template: spec: containers: - image: kodekloud/throw-dice name: throw-dice restartPolicy: Never backoffLimit: 25 \~\
Task ￼ Create a pod called my-busybox in the dev2406 namespace using the busybox image. The container should be called secret and should sleep for 3600 seconds.

The container should mount a read-only secret volume called secret-volume at the path /etc/secret-volume. The secret being mounted has already been created for you and is called dotfile-secret.

Make sure that the pod is scheduled on controlplane and no other node in the cluster.

apiVersion: v1 kind: Pod metadata: creationTimestamp: null labels: run: my-busybox name: my-busybox namespace: dev2406 spec: volumes:

* name: secret-volume secret: secretName: dotfile-secret nodeSelector: kubernetes.io/hostname: controlplane containers:
* command:
  * sleep args:
  * "3600" image: busybox name: secret volumeMounts:
  * name: secret-volume readOnly: true mountPath: "/etc/secret-volume"

my version: apiVersion: v1 kind: Pod metadata: creationTimestamp: null labels: run: my-busybox name: my-busybox spec: containers:

* image: busybox name: my-busybox resources: {} command: \["sleep", "3600"] volumeMounts:
  * name: secret-volume mountPath: "/etc/secret-volume" readOnly: true restartPolicy: Always volumes:
* name: secret-volume secret: secretName: dotfile-secret optional: true nodeName: controlplane status: {}

Task Create a single ingress resource called ingress-vh-routing. The resource should route HTTP traffic to multiple hostnames as specified below:

The service video-service should be accessible on http://watch.ecom-store.com:30093/video

The service apparels-service should be accessible on http://apparels.ecom-store.com:30093/wear

Here 30093 is the port used by the Ingress Controller

Solution Use the following YAML to create the ingress resource:

***

kind: Ingress apiVersion: networking.k8s.io/v1 metadata: name: ingress-vh-routing annotations: nginx.ingress.kubernetes.io/rewrite-target: / spec: rules:

* host: watch.ecom-store.com http: paths:
  * pathType: Prefix path: "/video" backend: service: name: video-service port: number: 8080
* host: apparels.ecom-store.com http: paths:
  * pathType: Prefix path: "/wear" backend: service: name: apparels-service port: number: 8080

6 / 14 Weight: 11 Create a service messaging-service to expose the redis deployment in the marketing namespace within the cluster on port 6379.

Use imperative commands

Service: messaging-service

Port: 6379

Use the right type of Service

Use the right labels

13 / 14 Weight: 6 Create a redis deployment using the image redis:alpine with 1 replica and label app=redis. Expose it via a ClusterIP service called redis on port 6379. Create a new Ingress Type NetworkPolicy called redis-access which allows only the pods with label access=redis to access the deployment.

controlplane \~ ➜ cat depl.yaml apiVersion: apps/v1 kind: Deployment metadata: creationTimestamp: null labels: app: redis name: redis spec: replicas: 1 selector: matchLabels: app: redis strategy: {} template: metadata: creationTimestamp: null labels: app: redis spec: containers: - image: redis:alpine name: redis resources: {} status: {}

controlplane \~ ➜ cat depl.yaml apiVersion: apps/v1 kind: Deployment metadata: creationTimestamp: null labels: app: redis name: redis spec: replicas: 1 selector: matchLabels: app: redis strategy: {} template: metadata: creationTimestamp: null labels: app: redis spec: containers: - image: redis:alpine name: redis resources: {} status: {}

Add a taint to the node node01 of the cluster. Use the specification below:

key: app\_type, value: alpha and effect: NoSchedule

Create a pod called alpha, image: redis with toleration to node01.

Task Create a new Ingress Resource for the service my-video-service to be made available at the URL: http://ckad-mock-exam-solution.com:30093/video.

To create an ingress resource, the following details are: -

annotation: nginx.ingress.kubernetes.io/rewrite-target: /

host: ckad-mock-exam-solution.com

path: /video

Once set up, the curl test of the URL from the nodes should be successful: HTTP 200

apiVersion: networking.k8s.io/v1 kind: Ingress metadata: name: my-video-service annotations: nginx.ingress.kubernetes.io/rewrite-target: / spec: ingressClassName: my-video-service rules:

* host: ckad-mock-exam-solution.com http: paths:
  * path: /video pathType: Prefix backend: service: name: my-video-service port: number: 8080 \~

k create ingress ingress --rule="\*=:"

JOB k create job --image=

tip on commands in containers:

command:

* "/bin/sh"
* "-c"
* "Something"

watch k get jobs

PersistentVolume

apiVersion: v1 kind: PersistentVolume metadata: name: custom-volume spec: capacity: storage: 50Mi accessModes: - ReadWriteMany persistentVolumeReclaimPolicy: Retain hostPath: path: /path/foo
