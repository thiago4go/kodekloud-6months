FROM python:3.10-alpine

WORKDIR /kodekloud-twelve-factors-app

COPY requirements.txt /kodekloud-twelve-factors-app

RUN pip install -r requirements.txt --no-cache-dir

COPY . /kodekloud-twelve-factors-app

CMD python app.py
