import sys
import logging
from concurrent import futures

import grpc

from api.v1 import timeline_pb2_grpc
from chii.config import config
from rpc.timeline_service import TimeLineService


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    timeline_pb2_grpc.add_TimeLineServiceServicer_to_server(TimeLineService(), server)
    server.add_insecure_port(f"0.0.0.0:{config.grpc_port}")
    print("Server started, listening on", config.grpc_port, flush=True)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    if "-h" in sys.argv or "--help" in sys.argv:
        print("timeline micro service")
        exit(0)
    print("starting grpc server", flush=True)
    logging.basicConfig()
    serve()
