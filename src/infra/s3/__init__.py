from typing import AsyncIterator
from dishka import Provider, Scope, alias, provide

from ..protocols import S3Storage
from .minio import MinioImageRepo


class S3Provider(Provider):
    scope = Scope.REQUEST

    def __init__(self):
        super().__init__()

    @provide
    def get_s3_storage(self) -> AsyncIterator[S3Storage]:
        return MinioImageRepo()

    image_storage = alias(source=MinioImageRepo, provides=S3Storage)
