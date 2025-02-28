FROM ghcr.io/astral-sh/uv:debian-slim@sha256:3c3ca15d7011789f6bd703acc8b8c2533da4ff94ce2d8281bf0420eb33db891f AS build

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
