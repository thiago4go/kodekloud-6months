# Docker Lab

1/15 How many images are in the host?

```
// Some code
docker images
docker images | wc -l
```

2/15 What is the size of the `ubuntu` image

```
// Some code
docker images | grep ubuntu
```

3/15  What is the tag on the newly pulled `NGINX` image?

```
// Some code
docker images | grep ngninx
```

4/15 What is the base image used in the Dockerfile?

Inspect the Dockerfile in the `webapp-color` directory.

```
// Some code
cat Dockerfile
FROM python:3.6

RUN pip install flask

COPY . /opt/

EXPOSE 8080

WORKDIR /opt

ENTRYPOINT ["python", "app.py"]
```

5/15 To what location within the container is the application code copied to during a Docker build?

Inspect the Dockerfile in the webapp-color directory.

6/15 When a container is created using the image built with this Dockerfile, what is the command used to `RUN` the application inside it.

8/15 Build a docker image using the Dockerfile and name it `webapp-color.` Notag to be specified

```
// Some code
docker build -t webapp-color .
```

9/15 Run an instance of the image `webapp-color` and publish port `8080` on the container to `8282` on the host.

```
// Some code
docker run -d -p 8282:8080 webapp-color
```

11/15 What is the base Operating System used by the `python:3.6` image?

If required, run an instance of the image to figure it out.

```
// Some code
docker run -it python:3.6 bash
cat /etc/os-release

```

15/15 Run a instalce of the new image `webapp-color:lite` and publish port 8080 on the container to 8383 on the host

```
// Some code
docker run -d -p 8383:8080 webapp-color:lite
```
