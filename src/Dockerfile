FROM python:3.7-alpine
MAINTAINER Sonia

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /src
COPY . /src
WORKDIR /src