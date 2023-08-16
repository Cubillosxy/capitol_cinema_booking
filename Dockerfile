FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /tmp/

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /code
WORKDIR /code



RUN pip install --upgrade pip

ADD requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY . /code/