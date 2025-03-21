from dataclasses import dataclass
from datetime import datetime

import boto3
from boto3.exceptions import Boto3Error
from pydantic import BaseModel

from infra.protocols import Boto3Repo


class S3StorageSettings(BaseModel):
    endpoint: str = "http://localhost:9001"
    bucket_name: str = "content-images"
    access_key: str | None = ""
    secret_key: str | None = ""
    session_token: str | None = None
    secure: bool = True
    region: str | None = None


@dataclass(frozen=True)
class FileInfo:
    content_type: str


@dataclass(frozen=True)
class FileDescr(FileInfo):
    name: str
    url: str
    size: int
    created_at: datetime


@dataclass(frozen=True)
class ImageDescr(FileDescr):
    width: int
    height: int


class Boto3FileRepo(Boto3Repo):

    def _create_descr(self, obj) -> FileDescr:
        return FileDescr(
            name=obj.object_name,
            content_type=obj.metadata["content-type"],
            url=f"{self.base_image_url}{self.bucket_name}/{obj.object_name}",
            size=obj.size,
            created_at=obj.last_modified,
        )


class Boto3ImageRepo(Boto3Repo):

    def _create_descr(self, obj) -> ImageDescr:
        return ImageDescr(
            name=obj.object_name,
            content_type=obj.metadata["content-type"],
            width=int(obj.metadata["X-Amz-Meta-Width"]),
            height=int(obj.metadata["X-Amz-Meta-Height"]),
            url=f"{self.base_image_url}{self.bucket_name}/{obj.object_name}",
            size=obj.size,
            created_at=obj.last_modified,
        )
