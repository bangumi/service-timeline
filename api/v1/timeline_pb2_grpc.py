# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from api.v1 import timeline_pb2 as api_dot_v1_dot_timeline__pb2

GRPC_GENERATED_VERSION = '1.66.2'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in api/v1/timeline_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class TimeLineServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Hello = channel.unary_unary(
                '/api.v1.TimeLineService/Hello',
                request_serializer=api_dot_v1_dot_timeline__pb2.HelloRequest.SerializeToString,
                response_deserializer=api_dot_v1_dot_timeline__pb2.HelloResponse.FromString,
                _registered_method=True)
        self.SubjectCollect = channel.unary_unary(
                '/api.v1.TimeLineService/SubjectCollect',
                request_serializer=api_dot_v1_dot_timeline__pb2.SubjectCollectRequest.SerializeToString,
                response_deserializer=api_dot_v1_dot_timeline__pb2.SubjectCollectResponse.FromString,
                _registered_method=True)
        self.SubjectProgress = channel.unary_unary(
                '/api.v1.TimeLineService/SubjectProgress',
                request_serializer=api_dot_v1_dot_timeline__pb2.SubjectProgressRequest.SerializeToString,
                response_deserializer=api_dot_v1_dot_timeline__pb2.SubjectProgressResponse.FromString,
                _registered_method=True)
        self.EpisodeCollect = channel.unary_unary(
                '/api.v1.TimeLineService/EpisodeCollect',
                request_serializer=api_dot_v1_dot_timeline__pb2.EpisodeCollectRequest.SerializeToString,
                response_deserializer=api_dot_v1_dot_timeline__pb2.EpisodeCollectResponse.FromString,
                _registered_method=True)


class TimeLineServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Hello(self, request, context):
        """Debug function
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubjectCollect(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubjectProgress(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EpisodeCollect(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TimeLineServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Hello': grpc.unary_unary_rpc_method_handler(
                    servicer.Hello,
                    request_deserializer=api_dot_v1_dot_timeline__pb2.HelloRequest.FromString,
                    response_serializer=api_dot_v1_dot_timeline__pb2.HelloResponse.SerializeToString,
            ),
            'SubjectCollect': grpc.unary_unary_rpc_method_handler(
                    servicer.SubjectCollect,
                    request_deserializer=api_dot_v1_dot_timeline__pb2.SubjectCollectRequest.FromString,
                    response_serializer=api_dot_v1_dot_timeline__pb2.SubjectCollectResponse.SerializeToString,
            ),
            'SubjectProgress': grpc.unary_unary_rpc_method_handler(
                    servicer.SubjectProgress,
                    request_deserializer=api_dot_v1_dot_timeline__pb2.SubjectProgressRequest.FromString,
                    response_serializer=api_dot_v1_dot_timeline__pb2.SubjectProgressResponse.SerializeToString,
            ),
            'EpisodeCollect': grpc.unary_unary_rpc_method_handler(
                    servicer.EpisodeCollect,
                    request_deserializer=api_dot_v1_dot_timeline__pb2.EpisodeCollectRequest.FromString,
                    response_serializer=api_dot_v1_dot_timeline__pb2.EpisodeCollectResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'api.v1.TimeLineService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('api.v1.TimeLineService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class TimeLineService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Hello(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/api.v1.TimeLineService/Hello',
            api_dot_v1_dot_timeline__pb2.HelloRequest.SerializeToString,
            api_dot_v1_dot_timeline__pb2.HelloResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SubjectCollect(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/api.v1.TimeLineService/SubjectCollect',
            api_dot_v1_dot_timeline__pb2.SubjectCollectRequest.SerializeToString,
            api_dot_v1_dot_timeline__pb2.SubjectCollectResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SubjectProgress(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/api.v1.TimeLineService/SubjectProgress',
            api_dot_v1_dot_timeline__pb2.SubjectProgressRequest.SerializeToString,
            api_dot_v1_dot_timeline__pb2.SubjectProgressResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def EpisodeCollect(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/api.v1.TimeLineService/EpisodeCollect',
            api_dot_v1_dot_timeline__pb2.EpisodeCollectRequest.SerializeToString,
            api_dot_v1_dot_timeline__pb2.EpisodeCollectResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
