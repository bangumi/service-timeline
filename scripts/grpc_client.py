import grpc
from sslog import logger

from api.v1 import timeline_pb2_grpc
from api.v1.timeline_pb2 import HelloRequest
from chii.config import config


def run() -> None:
    logger.info("healthy check")
    with grpc.insecure_channel(f"127.0.0.1:{config.grpc_port}") as channel:
        stub = timeline_pb2_grpc.TimeLineServiceStub(channel)
        stub.Hello(HelloRequest(name="client"))


if __name__ == "__main__":
    run()
