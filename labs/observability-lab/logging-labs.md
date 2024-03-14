# Logging Labs

2/4 A user - `USER5` - has expressed concerns accessing the application. Identify the cause of the issue.

Inspect the logs of the POD

```
k logs <pod-name> | grep USER5

```

4 / 4 A user is reporting issues while trying to purchase an item. Identify the user and the cause of the issue.

Inspect the logs of the webapp in the POD

```
k logs <pod-name> 
```
