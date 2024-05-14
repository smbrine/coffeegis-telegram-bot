from grpc import aio

from proto import (
    image_service_pb2,
    image_service_pb2_grpc,
)


class ImagesWrapper:
    def __init__(self, host: str) -> None:
        self.host = host

    async def PostImage(
        self,
    ):
        async with aio.insecure_channel(
            self.host
        ) as channel:
            stub = image_service_pb2.CityCafeServiceStub(
                channel
            )
            req = (
                image_service_pb2_grpc.PostImageRequest()
            )

            return await stub.PostImage(req)

    async def GetImage(self, uuid: str):
        async with aio.insecure_channel(
            self.host
        ) as channel:
            stub = image_service_pb2_grpc.ImageServiceStub(
                channel
            )
            req = (
                image_service_pb2.GetImageRequest(
                    uuid=uuid
                )
            )

            return await stub.GetImage(req)
