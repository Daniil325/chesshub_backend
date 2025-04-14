from abc import ABC, abstractmethod
from typing import BinaryIO


class S3Storage(ABC):
    base_url = "/media/"

    @abstractmethod
    async def exists(self, image_id: str) -> bool: ...

    @abstractmethod
    async def upload(
        self, filename: str, file: BinaryIO, size: int | None = None
    ) -> str: ...
