FROM python:3.9.12-alpine

# Console output in real time and no *.pyc files
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt
COPY ./.env /src/.env

RUN apk add --update --no-cache --virtual .tmp gcc libc-dev \
    linux-headers postgresql-dev postgresql-client
RUN apk add build-base
RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./business_manage /src