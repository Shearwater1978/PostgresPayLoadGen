FROM python:3.8

MAINTAINER Aleksandr uglykoyote@gmail.com

ENV PERSON_COUNT = 10 \
    BEHAVIOR_MODEL = push \
    SEND_TO_API = false

WORKDIR /app
ADD geninfo.py /app/
ADD requirements.txt

RUN pip install -r requirements.txt
