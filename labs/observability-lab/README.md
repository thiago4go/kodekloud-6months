# Observability Lab

Update both the pods with a livenessProbe using the given spec

\
6 / 13 Update the newly created pod 'simple-webapp-2' with a readinessProbe using the given spec

Spec is given on the below. Do not modify any other properties of the pod.

Pod Name: simple-webapp-2

Image Name: kodekloud/webapp-delayed-start

Readiness Probe: httpGet

Http Probe: /ready

Http Port: 8080



11/13



Delete and recreate the PODs.

\-

Check

\-Next

Pod Name: simple-webapp-1

Image Name: kodekloud/webapp-delayed-start

Liveness Probe: httpGet

Http Probe: /live

Http Port: 8080

Period Seconds: 1

Initial Delay: 80

Pod Name: simple-webapp-2

Image Name: kodekloud/webapp-delayed-start

Liveness Probe: httpGet

Http Probe: /live

Http Port: 8080

Initial Delay: 80

Period Seconds: 1
