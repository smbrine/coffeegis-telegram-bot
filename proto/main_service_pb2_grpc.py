# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from proto import (
    main_service_pb2 as proto_dot_main__service__pb2,
)


class CityCafeServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListCafesPerCity = channel.unary_unary(
            "/main.CityCafeService/ListCafesPerCity",
            request_serializer=proto_dot_main__service__pb2.ListCafesPerCityRequest.SerializeToString,
            response_deserializer=proto_dot_main__service__pb2.ListCafesPerCityResponse.FromString,
        )
        self.SearchCafesByQueryPerCity = channel.unary_unary(
            "/main.CityCafeService/SearchCafesByQueryPerCity",
            request_serializer=proto_dot_main__service__pb2.SearchCafesByQueryPerCityRequest.SerializeToString,
            response_deserializer=proto_dot_main__service__pb2.SearchCafesByQueryPerCityResponse.FromString,
        )


class CityCafeServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ListCafesPerCity(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(
            grpc.StatusCode.UNIMPLEMENTED
        )
        context.set_details(
            "Method not implemented!"
        )
        raise NotImplementedError(
            "Method not implemented!"
        )

    def SearchCafesByQueryPerCity(
        self, request, context
    ):
        """Missing associated documentation comment in .proto file."""
        context.set_code(
            grpc.StatusCode.UNIMPLEMENTED
        )
        context.set_details(
            "Method not implemented!"
        )
        raise NotImplementedError(
            "Method not implemented!"
        )


def add_CityCafeServiceServicer_to_server(
    servicer, server
):
    rpc_method_handlers = {
        "ListCafesPerCity": grpc.unary_unary_rpc_method_handler(
            servicer.ListCafesPerCity,
            request_deserializer=proto_dot_main__service__pb2.ListCafesPerCityRequest.FromString,
            response_serializer=proto_dot_main__service__pb2.ListCafesPerCityResponse.SerializeToString,
        ),
        "SearchCafesByQueryPerCity": grpc.unary_unary_rpc_method_handler(
            servicer.SearchCafesByQueryPerCity,
            request_deserializer=proto_dot_main__service__pb2.SearchCafesByQueryPerCityRequest.FromString,
            response_serializer=proto_dot_main__service__pb2.SearchCafesByQueryPerCityResponse.SerializeToString,
        ),
    }
    generic_handler = (
        grpc.method_handlers_generic_handler(
            "main.CityCafeService",
            rpc_method_handlers,
        )
    )
    server.add_generic_rpc_handlers(
        (generic_handler,)
    )


# This class is part of an EXPERIMENTAL API.
class CityCafeService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ListCafesPerCity(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/main.CityCafeService/ListCafesPerCity",
            proto_dot_main__service__pb2.ListCafesPerCityRequest.SerializeToString,
            proto_dot_main__service__pb2.ListCafesPerCityResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def SearchCafesByQueryPerCity(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/main.CityCafeService/SearchCafesByQueryPerCity",
            proto_dot_main__service__pb2.SearchCafesByQueryPerCityRequest.SerializeToString,
            proto_dot_main__service__pb2.SearchCafesByQueryPerCityResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )


class ArbitraryJSONServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetArbitraryJSON = channel.unary_unary(
            "/main.ArbitraryJSONService/GetArbitraryJSON",
            request_serializer=proto_dot_main__service__pb2.GetArbitraryJSONRequest.SerializeToString,
            response_deserializer=proto_dot_main__service__pb2.GetArbitraryJSONResponse.FromString,
        )


class ArbitraryJSONServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetArbitraryJSON(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(
            grpc.StatusCode.UNIMPLEMENTED
        )
        context.set_details(
            "Method not implemented!"
        )
        raise NotImplementedError(
            "Method not implemented!"
        )


def add_ArbitraryJSONServiceServicer_to_server(
    servicer, server
):
    rpc_method_handlers = {
        "GetArbitraryJSON": grpc.unary_unary_rpc_method_handler(
            servicer.GetArbitraryJSON,
            request_deserializer=proto_dot_main__service__pb2.GetArbitraryJSONRequest.FromString,
            response_serializer=proto_dot_main__service__pb2.GetArbitraryJSONResponse.SerializeToString,
        ),
    }
    generic_handler = (
        grpc.method_handlers_generic_handler(
            "main.ArbitraryJSONService",
            rpc_method_handlers,
        )
    )
    server.add_generic_rpc_handlers(
        (generic_handler,)
    )


# This class is part of an EXPERIMENTAL API.
class ArbitraryJSONService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetArbitraryJSON(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/main.ArbitraryJSONService/GetArbitraryJSON",
            proto_dot_main__service__pb2.GetArbitraryJSONRequest.SerializeToString,
            proto_dot_main__service__pb2.GetArbitraryJSONResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
