from api.v1.timeline_pb2 import HelloRequest
from rpc.timeline_service import TimeLineService


def test_Hello():
    assert (
        TimeLineService()
        .Hello(HelloRequest(name="nn"), None)
        .message.endswith(": hello nn")
    )
