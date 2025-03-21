from abc import ABC, abstractmethod
import os
from pathlib import Path
import re
from typing import BinaryIO


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


class Boto3Repo[T](ABC):
    base_url = "/media/"

    @abstractmethod
    async def exists(self, image_id: str) -> bool: ...

    @abstractmethod
    async def upload(
        self, filename: str, file: BinaryIO, size: int | None = None
    ) -> str: ...

    @abstractmethod
    async def download(self, image_id: str) -> bytes: ...

    async def create_new_id(self, filename: str) -> str:
        identity = secure_filename(filename)
        stem = Path(identity).stem
        suffix = Path(identity).suffix
        counter = 0

        while await self.exists(identity):
            counter += 1
            identity = f"{stem}-{counter}{suffix}"
        return identity

    async def get(self, image_id: str) -> T | None: ...

    @abstractmethod
    def _create_descr(self, obj) -> T: ...
