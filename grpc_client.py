import logging

import grpc

from api.v1 import timeline_pb2_grpc
from api.v1.timeline_pb2 import Subject, SubjectCollectRequest, SubjectProgressResponse


def run():
    print("Will try to greet world ...")
    with grpc.insecure_channel("127.0.0.1:5000") as channel:
        stub = timeline_pb2_grpc.TimeLineServiceStub(channel)
        response: SubjectProgressResponse = stub.SubjectCollect(
            SubjectCollectRequest(
                user_id=100,
                subject=Subject(
                    id=88,
                    name="nn",
                    image="image image",
                    type=2,
                    name_cn="name cn",
                    series=False,
                    eps_total=0,
                    vols_total=0,
                ),
                comment="",
                collection=1,
                rate=0,
            )
        )
    print("Greeter client received:", response.ok)


if __name__ == "__main__":
    logging.basicConfig()
    run()
