from typing import AsyncIterator
import aiohttp
from dishka import Provider, Scope, alias, provide

from src.settings import settings

from ..protocols import S3Storage
from .minio import MinioImageRepo


class S3Provider(Provider):
    scope = Scope.REQUEST

    def __init__(self):
        super().__init__()

    @provide
    async def get_s3_storage(self) -> AsyncIterator[MinioImageRepo]:
        async with aiohttp.ClientSession() as session:
            yield MinioImageRepo(settings.storage, session)

    image_storage = alias(source=MinioImageRepo, provides=S3Storage)
