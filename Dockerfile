FROM ghcr.io/astral-sh/uv:debian-slim@sha256:3c3ca15d7011789f6bd703acc8b8c2533da4ff94ce2d8281bf0420eb33db891f AS build

WORKDIR /app

COPY uv.lock pyproject.toml ./

RUN uv export --no-group dev --frozen --no-emit-project > /app/requirements.txt

FROM python:3.10-slim@sha256:f680fc3f447366d9be2ae53dc7a6447fe9b33311af209225783932704f0cb4e7

ENTRYPOINT [ "python", "-m", "start_grpc_server" ]

ENV PIP_ROOT_USER_ACTION=ignore
ENV PYTHONPATH=/app
WORKDIR /app

COPY --from=build /app/requirements.txt .

RUN pip install --only-binary=:all: --no-cache --no-deps -r requirements.txt

COPY . .
