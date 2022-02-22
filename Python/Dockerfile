#FROM python:3.8
FROM python:3.8.11-bullseye

MAINTAINER Aleksandr uglykoyote@gmail.com

ENV PERSON_COUNT=10
ENV BEHAVIOR_MODEL="push"
ENV SEND_TO_API="false"

ARG USERNAME=notroot
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

USER notroot
WORKDIR /app
COPY geninfo.py /app/
COPY requirements.txt /app/

RUN pip install -r requirements.txt --no-warn-script-location

ENTRYPOINT ["python","geninfo.py"]
