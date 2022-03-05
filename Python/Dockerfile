#FROM python:3.8
FROM python:3.8.11-bullseye

MAINTAINER Aleksandr uglykoyote@gmail.com

ENV PERSON_COUNT=10
ENV BEHAVIOR_MODEL="push"
ENV SEND_TO_API="false"

ENV DB_USER_NAME=test_user
ENV DB_USER_PASS=test_pass
ENV DB_USER_DB=test_db
ENV DB_USER_PG_HOST=127.0.0.1
ENV DB_USER_PG_PORT=5432
ENV RANDOM_FACTOR=0
ENV SEND_TO_CONSOLE=True

ARG USERNAME=notroot
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt update \
    && apt install net-tools \
    && rm -rf /var/lib/apt/lists 

USER notroot
WORKDIR /opt/
COPY ./aux_scripts/requirements.txt .
COPY ./sql/ .
RUN pip install -r ./requirements.txt --no-warn-script-location

WORKDIR /app
COPY ./aux_scripts/ /app/

ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
