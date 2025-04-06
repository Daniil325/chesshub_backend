import re
import os.path
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import AsyncGenerator, BinaryIO

import aiohttp
import imgspy
from miniopy_async import Minio, S3Error
from pydantic import BaseModel

from src.infra.protocols import S3Storage


class S3StorageSettings(BaseModel):
    endpoint: str
    bucket_name: str = "content-images"
    access_key: str | None = None
    secret_key: str | None = None
    session_token: str | None = None
    secure: bool = True
    region: str | None = None


_filename_ascii_strip_re = re.compile(r"[^A-Za-z0-9_.-]")


def secure_filename(filename: str) -> str:
    """
    From Werkzeug secure_filename.
    """

    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, " ")

    normalized_filename = _filename_ascii_strip_re.sub("", "_".join(filename.split()))
    filename = str(normalized_filename).strip("._")
    return filename


@dataclass(frozen=True)
class ImageInfo:
    content_type: str
    width: int
    height: int


@dataclass(frozen=True)
class ImageDescr(ImageInfo):
    name: str
    url: str
    size: int
    created_at: datetime


class MinioImageRepo(S3Storage):
    base_image_url = "/media/"

    def __init__(
        self, minio_settings: S3StorageSettings, session: aiohttp.ClientSession
    ):
        self.client = Minio(
            endpoint=minio_settings.endpoint,
            access_key=minio_settings.access_key,
            secret_key=minio_settings.secret_key,
            secure=minio_settings.secure,
        )
        self.bucket_name = minio_settings.bucket_name
        self._session = session

    async def list(
        self, prefix: str | None = None, start_after: str | None = None
    ) -> AsyncGenerator[ImageDescr, None]:
        for obj in await self.client.list_objects(
            self.bucket_name,
            prefix=prefix,
            start_after=start_after,
            include_user_meta=True,
        ):
            yield self._create_image_descr(obj)

    async def get(self, image_id: str) -> ImageDescr:
        try:
            return self._create_image_descr(
                await self.client.stat_object(self.bucket_name, image_id)
            )
        except S3Error as e:
            if e.code == "NoSuchKey":
                raise f"Image {image_id} not found in storage"
            raise

    def _create_image_descr(self, obj) -> ImageDescr:
        return ImageDescr(
            name=obj.object_name,
            content_type=obj.metadata["content-type"],
            width=int(obj.metadata["X-Amz-Meta-Width"]),
            height=int(obj.metadata["X-Amz-Meta-Height"]),
            url=f"{self.base_image_url}{self.bucket_name}/{obj.object_name}",
            size=obj.size,
            created_at=obj.last_modified,
        )

    async def exists(self, image_id: str) -> bool:
        try:
            return bool(await self.client.stat_object(self.bucket_name, image_id))
        except S3Error as e:
            if e.code == "NoSuchKey":
                return False
            raise

    async def upload(
        self, filename: str, file: BinaryIO, size: int | None = None
    ) -> str:
        identity = await self.create_new_id(filename)
        if not size:
            size = self._get_file_size(file)
        img_info = self._get_image_info(file)
        await self.client.put_object(
            self.bucket_name,
            identity,
            file,
            length=size,
            content_type=img_info.content_type,
            metadata={"height": img_info.height, "width": img_info.width},
        )
        return identity

    @staticmethod
    def _get_file_size(file: BinaryIO) -> int:
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0, os.SEEK_SET)
        return size

    @staticmethod
    def _get_image_info(file: BinaryIO) -> ImageInfo:
        info = imgspy.info(file)
        file.seek(0, os.SEEK_SET)
        type = {"jpg": "jpeg"}.get(info["type"], info["type"])
        return ImageInfo(
            content_type=f"image/{type}", width=info["width"], height=info["height"]
        )

    async def download(self, image_id: str) -> bytes:
        response = await self.client.get_object(
            self.bucket_name, image_id, self._session
        )
        return await response.read()

    async def create_new_id(self, filename: str) -> str:
        identity = secure_filename(filename)
        stem = Path(identity).stem
        suffix = Path(identity).suffix
        counter = 0

        while await self.exists(identity):
            counter += 1
            identity = f"{stem}-{counter}{suffix}"

        return identity
