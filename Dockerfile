FROM ubuntu:20.04
WORKDIR /code

ADD requirements.txt /code

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip \
    vim \
    python3-pymysql && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt

EXPOSE 5000
