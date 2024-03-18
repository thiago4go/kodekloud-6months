# 🔹 POD Design

## Labels and Selectors



* Criterias to classify, label and filter, selectors, objects



```
labels:
  key: value
  key2: value2
```

```
k get pods --selector key=value
```



On an ReplicaSet

```
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: simple-web-app
  lables:
    app: App1
    function: Front-end
spec:
  replicas: 3
  selector:
    matchLabels:
      app: App1
    template:
      metadata:
        labels:
          app: App1
          function: Front-end
        spec:
          containers:
          - name: simple-webapp
            image: simple-webapp
```

{% hint style="info" %}
Annotations: It is used only for notes
{% endhint %}



## Rolling Updates & Rollbaks

Rollout and versioning

Revision are create at any deployment applied

*   Deployment Strategy

    * Recreate Strategy -> donwtime
    * Rolling update -> default strategy
      * Blue/Green, it deploy a new version but do not allow trafic until all test passeds, making the chage on the Selector in the service.
    * Canary Strategy
      * Deploy only partially a new version and test, it have a caveate since we cannot control the range of trafic to the canary pod.



We can update many things, but it is best to update the file and them appy

to rolllback

```
k rollout undo deployment/myapp-deployment
```

To rollback to specific revision we will use the `--to-revision` flag.



to check status of rollout

```
k rollout status deployment/myapp-deployment
k rollout history deployment/myapp-deployment
```



## Jobs and CronJobs

Types of workloads: Web, applications and databases, these keep running. Also have scripts and reporting that usually carry specific task and then finish, living for a short time.



Kubernetes wants to make the container to run forever

```
restartPolice: Always

restartPolice: Never
```



A Job is similiar to ReplicaSet in a sense of creating multiple pods, but it is goal is to run a specific Task/Job

{% code title="job-definition" overflow="wrap" %}
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: math-add-job
spec:
  # Set how many pods
  completions: 3
  # The default is one pod at time, but can set to run in parallele
  parallelism: 3
  template:
    spec:
      containers:
      - name: math-add
        image: ubuntu
        command: ['expr','3','+','2']
      restartPolicy: Never
```
{% endcode %}



### CronJob

Similar to CronJob in Linux, it mean that we can schedule a job to run arbitraly



<figure><img src="../.gitbook/assets/image (10) (1).png" alt=""><figcaption></figcaption></figure>

Take extra

{% code title="" overflow="wrap" %}
```yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: reporting-cron-job
spec:
    schedule: "*/1 * * * *"
    jobTemplate:
      spec:
        # Set how many pods
        completions: 3
        # The default is one pod at time, but can set to run in parallele
        parallelism: 3
        template:
          spec:
            containers:
            - name: math-add
              image: ubuntu
              command: ['expr','3','+','2']
            restartPolicy: Never
```
{% endcode %}









