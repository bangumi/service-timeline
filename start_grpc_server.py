import logging
import sys
from concurrent import futures

import grpc
import sslog
from sslog import logger

from api.v1 import timeline_pb2_grpc
from chii.config import config
from rpc.timeline_service import TimeLineService


def start_server():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=config.grpc_max_workers)
    )
    timeline_pb2_grpc.add_TimeLineServiceServicer_to_server(TimeLineService(), server)
    server.add_insecure_port(f"0.0.0.0:{config.grpc_port}")
    logger.info("Server started, listening on {}", config.grpc_port)
    server.start()
    server.wait_for_termination()


def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        print("timeline micro service")
        sys.exit(0)
    logger.info("starting grpc server")
    logging.basicConfig(
        handlers=[
            sslog.InterceptHandler(
                level=logging.NOTSET if config.debug else logging.INFO
            )
        ]
    )
    start_server()


if __name__ == "__main__":
    main()
