from typing import AsyncIterable
import aiohttp
from dishka import Provider, Scope, provide

from ..protocols import FileRepo, ImageRepo
from .minio import MinioFileRepo, MinioImageRepo


class S3Provider(Provider):
    scope = Scope.REQUEST

    def __init__(self, settings: "Settings"):
        super().__init__()
        self.settings = settings
        
    @provide
    async def get_session(self) -> AsyncIterable[aiohttp.ClientSession]:
        async with aiohttp.ClientSession() as session:
            yield session
            

    @provide
    async def get_image_storage(self, session: aiohttp.ClientSession) -> ImageRepo:
        return MinioImageRepo(self.settings.storage, session)

    @provide
    async def get_file_storage(self, session: aiohttp.ClientSession) -> FileRepo:
        return MinioFileRepo(self.settings.storage, session)
