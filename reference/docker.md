# 📦 Docker

Container Definition:

A container is a standard unit of software that packages up code and all its dependencies so the application runs quickly and reliably from one computing environment to another. A Docker container image is a lightwight, standalone, executable package of software taht includdes everything needed to run an application: code, runtime, system tools, system libraries and settings.



How to containarize a we applications

1 OS - Ubuntu

2 Update apt repo

3 Install dependencies using `apt`

4 install Python dependencies using `pip`

5 Copy source code to /opt directory

6 run the web server using `flask`

{% code title="Dockerfile" %}
```docker
FROM Ubuntu

RUN apt-get update
RUN atp-get install python

RUN pip install flask
RUN pip install flask-mysql

COPY . /opt/source-code

ENTRYPOINT FLASK_APP=/otp/source-code/app.py frask run
```
{% endcode %}

```
// Some code
docker build Dockerfile -t thiago4go/my-custom-app

docker push thiago4go/my-custom-app
```

Layered Architecture

`docker history <image-name>`

All layer is cached
