# ⚙️ Configurantion

Commands and Arguments in Docker

`docker run <image>`

`docker run <image> <command> <parameter>`

{% hint style="info" %}
ENTRYPOINT is how the application starts
{% endhint %}

Commands and Arguments in K8S

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

Enviroment Variable

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

ConfigMaps

```
// literal
k create configmap <config-name> --from-literal=<key>=<value>
// from file
k create configmap <config-name> --from-file=app.config.properties
```

declarative way

{% code title="config-map.yaml" %}
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_COLOR: blue
  APP_MODE: prod
```
{% endcode %}

```
k apply -f config-map.yaml
```

Inject ConfiMap Env Variable in a pod via `envFrom`

<figure><img src="../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>
