FROM python:3.12.2-alpine as base

RUN apk update && apk upgrade

RUN apk add curl nano gcc python3-dev musl-dev linux-headers

COPY . /app
WORKDIR /app

ENV POETRY_VERSION=1.7.1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  PYTHONPATH=/app

RUN pip install -U poetry

ENV PATH=/usr/local/bin:$PATH

RUN python3 -m poetry install --no-root
