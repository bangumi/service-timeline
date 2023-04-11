import sys
import json
import time
import logging
import threading
from typing import Optional
from concurrent import futures

import grpc
import etcd3
from etcd3 import Lease
from loguru import logger
from etcd3.utils import retry

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

        self.key = f"{config.etcd_prefix}/timeline/{config.node_id}".encode()
        self.value = json.dumps(
            {
                "Addr": config.external_address + ":" + str(config.grpc_port),
                "Metadata": None,
            }
        )
        self.lease: Optional[Lease] = None

        self.announce()

        self.stop = 0

    def announce(self):
        logger.info("announce node")
        self.lease = self.etcd.Lease(ttl=10)
        self.lease.grant()
        self.etcd.put(self.key, self.value, lease=self.lease.ID)

    def need_announce(self) -> bool:
        r = self.etcd.range(self.key).kvs
        if not r:
            return True

        return self.key not in [x.key for x in r]

    def run(self) -> None:
        while not self.stop:
            time.sleep(5)
            if self.need_announce():
                logger.info("old key not exists, re-create key/value pair")
                self.announce()
            else:
                retry(self.lease.keepalive_once, max_tries=3)


def start_server():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=config.grpc_max_workers)
    )
    timeline_pb2_grpc.add_TimeLineServiceServicer_to_server(TimeLineService(), server)
    server.add_insecure_port(f"0.0.0.0:{config.grpc_port}")
    logger.info("Server started, listening on {}", config.grpc_port)
    server.start()
    if not config.etcd_addr:
        logger.info("etcd not configured")
        server.wait_for_termination()
    else:
        logger.info(
            "announce with etcd, announced addr: {}:{}",
            config.external_address,
            config.grpc_port,
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
    logger.info("starting grpc server")
    logging.basicConfig()
    start_server()


if __name__ == "__main__":
    main()
