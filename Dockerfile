FROM ghcr.io/astral-sh/uv:debian-slim@sha256:3ac4e2ef46fd5a0fb0cf5af9a421435513fec1b2a66e1379a7981dc03470fd33 AS build

WORKDIR /app

COPY uv.lock pyproject.toml ./

RUN uv export --no-group dev --frozen --no-emit-project > /app/requirements.txt

FROM python:3.10-slim@sha256:66aad90b231f011cb80e1966e03526a7175f0586724981969b23903abac19081

ENTRYPOINT [ "python", "-m", "start_grpc_server" ]

ENV PIP_ROOT_USER_ACTION=ignore
ENV PYTHONPATH=/app
WORKDIR /app

COPY --from=build /app/requirements.txt .

RUN pip install --only-binary=:all: --no-cache --no-deps -r requirements.txt

COPY . .
