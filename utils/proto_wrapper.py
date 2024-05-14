from grpc import aio

from proto import (
    main_service_pb2,
    main_service_pb2_grpc,
)


class ProtoWrapper:
    def __init__(self, host: str) -> None:
        self.host = host

    async def ListCafesPerCity(
        self,
        lat: float,
        lon: float,
        len: int = 5,
        page: int = 0,
    ):
        async with aio.insecure_channel(
            self.host
        ) as channel:
            stub = main_service_pb2_grpc.CityCafeServiceStub(
                channel
            )
            req = main_service_pb2.ListCafesPerCityRequest(
                latitude=lat,
                longitude=lon,
                len=len,
                page=page,
            )

            return await stub.ListCafesPerCity(
                req
            )

    async def SearchCafesByQueryPerCity(
        self,
        query: str,
        lat: float,
        lon: float,
        len: int = 3,
        page: int = 0,
    ):
        async with aio.insecure_channel(
            self.host
        ) as channel:
            stub = main_service_pb2_grpc.CityCafeServiceStub(
                channel
            )
            req = main_service_pb2.SearchCafesByQueryPerCityRequest(
                query=query,
                latitude=lat,
                longitude=lon,
                len=len,
                page=page,
            )

            return await stub.SearchCafesByQueryPerCity(
                req
            )
