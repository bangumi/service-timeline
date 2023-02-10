import sys
import json
import time
import logging
import threading
from concurrent import futures

import grpc
import etcd3
from loguru import logger

from api.v1 import timeline_pb2_grpc
from chii.config import config
from rpc.timeline_service import TimeLineService


class Register(threading.Thread):
    """
    参照 etcd 的文档

    https://etcd.io/docs/v3.5/dev-guide/grpc_naming/

    go 有相关的 sdk，但是 python 没有。
    """

    def __init__(self):
        super().__init__()
        self.etcd = etcd3.Client(
            protocol=config.etcd_addr.scheme,
            host=config.etcd_addr.host,
            port=config.etcd_addr.port,
        )

        self.lease = self.etcd.Lease(ttl=5)
        self.lease.grant()
        self.etcd.put(
            f"{config.etcd_prefix}/timeline/{config.node_id}",
            json.dumps(
                {
                    "Addr": config.external_address + ":" + str(config.grpc_port),
                    "Metadata": None,
                }
            ),
            lease=self.lease.ID,
        )
        self.stop = 0

    def run(self) -> None:
        while True and self.stop == 0:
            time.sleep(2)
            self.lease.keepalive_once()


def start_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    timeline_pb2_grpc.add_TimeLineServiceServicer_to_server(TimeLineService(), server)
    server.add_insecure_port(f"0.0.0.0:{config.grpc_port}")
    print("Server started, listening on", config.grpc_port, flush=True)
    server.start()
    if not config.etcd_addr:
        logger.info("etcd not configured")
        server.wait_for_termination()
    else:
        logger.info(
            f"announce with etcd, announced addr: {config.external_address}:{config.grpc_port}"
        )
        r = Register()
        r.start()
        try:
            while 1:
                time.sleep(3600)
        except KeyboardInterrupt:
            r.stop = 1
            # 保证线程执行结束了
            server.stop(3)
            time.sleep(3)


def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        print("timeline micro service")
        exit(0)
    print("starting grpc server", flush=True)
    logging.basicConfig()
    start_server()


if __name__ == "__main__":
    main()
