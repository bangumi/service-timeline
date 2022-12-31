import logging

import grpc

from api.v1 import timeline_pb2_grpc
from api.v1.timeline_pb2 import HelloRequest, HelloResponse


def run():
    print("Will try to greet world ...")
    with grpc.insecure_channel("grpc.omv.trim21.me:9003") as channel:
        stub = timeline_pb2_grpc.TimeLineServiceStub(channel)
        response: HelloResponse = stub.Hello(HelloRequest(name="tt"))
    print("Greeter client received:", response.message)


if __name__ == "__main__":
    logging.basicConfig()
    run()
