# Lab #1

3/10 Create a pod with the ubuntu image to run a container to sleep for 5000 seconds. Modify the file `ubuntu-sleeper-2.yaml`.

{% code title="ubuntu-sleeper-2.yaml" %}
```
apiVersion: v1
kind: Pod 
metadata:
  name: ubuntu-sleeper-2
spec:
  containers:
  - name: ubuntu
    image: ubuntu
    command: ["sleep"]
    args: ["5000"]
  
```
{% endcode %}

4/10 Create a pod using the file named `ubuntu-sleeper-3.yaml`. There is something wrong with it. Try to fix it!

```
apiVersion: v1
kind: Pod 
metadata:
  name: ubuntu-sleeper-3
spec:
  containers:
  - name: ubuntu
    image: ubuntu
    command: ["sleep","1200"]
```

10/10 Create a pod with the five spec. set the given command arguments to charge it to `green`

```
// Some code
k run webapp-green --image=kodekloud/webapp-color -- --color green
```
