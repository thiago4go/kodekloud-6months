# Pod Desing Labs

Count Objects

```
k get pods --selector env=dev --no-headers | wc -l
```



Multi selectos:

```
k get pods --selector env=prod,bu=finance,tier=frontend
```

matchLabels and Label should be equal to bind Services and Objects



8 / 13

Let us try that. Upgrade the application by setting the image on the deployment to `kodekloud/webapp-color:v2`

Do not delete and re-create the deployment. Only set the new image name for the existing deployment.

```
k set image deployment/frontend simple-webapp=kodekloud/webapp-color:v2
```



5 / 10 - Canary Strategy

A new deployment called `frontend-v2` has been created in the default namespace using the image `kodekloud/webapp-color:v2`. This deployment will be used to test a newer version of the same app. Configure the deployment in such a way that the service called `frontend-service` routes less than 20% of traffic to the new deployment.\
Do not increase the replicas of the `frontend` deployment.



```
k scale deployment --replicas=1 frontend-v2
```



2 / 9

Create a Job using this POD definition file or from the imperative command and look at how many attempts does it take to get a `'6'`.

Use the specification given on the below.

Job Name: throw-dice-job

Image Name: kodekloud/throw-dice

```

controlplane ~ ➜  cat job.yaml 
apiVersion: batch/v1
kind: Job
metadata:
  creationTimestamp: null
  name: throw-dice-job
spec:
  completions: 3
  parallelism: 3
  backoffLimit: 10000 
  template:
    metadata:
      creationTimestamp: null
    spec:
      containers:
      - image: kodekloud/throw-dice
        name: throw-dice-job
        resources: {}
      restartPolicy: Never
status: {}

```



9 / 9 Let us now schedule that job to run at 21:30 hours every day.

Create a CronJob for this.

CronJob Name: throw-dice-cron-job

Image Name: kodekloud/throw-dice

Schedule: 30 21 \* \* \*

{% code overflow="wrap" %}
```
k create cronjob throw-dice-cron-job --image kodekloud/throw-dice  --schedule="30 21 * * *" --dry-run=client -o yaml > cronjob.yaml
```
{% endcode %}



```
controlplane ~ ➜  cat cronjob.yaml 
apiVersion: batch/v1
kind: CronJob
metadata:
  creationTimestamp: null
  name: throw-dice-cron-job
spec:
  jobTemplate:
    metadata:
      creationTimestamp: null
      name: throw-dice-cron-job
    spec:
      completions: 3
      parallelism: 3
      backoffLimit: 10000
      template:
        metadata:
          creationTimestamp: null
        spec:
          containers:
          - image: kodekloud/throw-dice
            name: throw-dice-job

          restartPolicy: Never
  schedule: 30 21 * * *
status: {}

```

