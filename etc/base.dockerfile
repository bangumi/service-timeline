### convert poetry.lock to requirements.txt ###

FROM python:3.11-slim AS poetry

WORKDIR /app
COPY . ./
COPY pyproject.toml poetry.lock ./

RUN pip install poetry &&\
  poetry export -f requirements.txt --output requirements.txt

### pip deps ###

FROM python:3.11-slim as builder

WORKDIR /app


### binary ###

FROM powerman/dockerize:0.17.0 AS dockerize

### final image ###
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY --from=dockerize /usr/local/bin/dockerize /usr/bin/dockerize

COPY --from=poetry /app/requirements.txt ./requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

WORKDIR /app

ENTRYPOINT [ "python", "./start_grpc_server.py" ]
