FROM ubuntu:20.04
WORKDIR /code

ADD requirements.txt /code

RUN apt-get update
RUN apt-get install -y python3-pip
RUN apt-get install -y git
RUN apt-get install -y make
RUN apt-get install -y gcc
RUN apt-get install -y --no-install-recommends vim
RUN apt-get install -y --no-install-recommends python3-pymysql

RUN pip3 install -r requirements.txt

EXPOSE 5000