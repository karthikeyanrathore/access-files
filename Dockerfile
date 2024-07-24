FROM python:3.6-slim as base
LABEL author="<karthikerathore@gmail.com>"

WORKDIR /home

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libncursesw5-dev openssl netcat-traditional \
    libssl-dev libsqlite3-dev tk-dev libgdbm-dev \
    libc6-dev libbz2-dev libffi-dev python3-dev python3-pip \
    libxml2-dev libxslt1-dev zlib1g zlib1g-dev python3-lxml \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt  /requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt

COPY ./access_files /home/access_files/
COPY ./wait-for.sh /home/