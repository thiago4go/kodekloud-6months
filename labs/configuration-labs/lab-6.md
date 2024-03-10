# Lab #6

3/7  Another pod called `elephant` has been deployed in the default namespace. It fails to get to a running state. Inspect this pod and identify the `Reason` why it is not running.\


check status

```
k describe pod elephant 
```

{% code overflow="wrap" %}
```
  1
    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       OOMKilled
      Exit Code:    1
      Started:      Sun, 10 Mar 2024 00:31:18 +0000
      Finished:     Sun, 10 Mar 2024 00:31:18 +0000
```
{% endcode %}







