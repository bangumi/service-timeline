FROM base-image

WORKDIR /app

ARG ARG_REF=""

ENV REF=$ARG_REF

COPY . ./

ENTRYPOINT [ "python", "./scripts/grpc_server.py" ]
