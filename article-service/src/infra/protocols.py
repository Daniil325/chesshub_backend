from abc import ABC, abstractmethod
from typing import Any, BinaryIO


# репозиторий для бд
class AbstractRepository(ABC):
    @abstractmethod
    async def insert(self, item: dict[str, Any]) -> None: ...

    @abstractmethod
    async def update(self, id: str | int, changes: dict[str, Any]) -> None: ...

    @abstractmethod
    async def delete(self, id: str | int) -> None: ...


# класс для чтения данных (Query)
class AbstractReader(ABC):
    @abstractmethod
    async def fetch_list(
        self, filter: str, order: str, page: int, per_page: int
    ) -> list: ...

    @abstractmethod
    async def fetch_one(self, id: str | int): ...


class S3Storage(ABC):
    base_url = "/media/"

    @abstractmethod
    async def exists(self, image_id: str) -> bool: ...

    @abstractmethod
    async def upload(
        self, filename: str, file: BinaryIO, size: int | None = None
    ) -> str: ...

    @abstractmethod
    async def get(self, image_id: str): ...

    @abstractmethod
    async def download(self, file_id: str) -> bytes: ...

    @abstractmethod
    async def create_new_id(self, filename: str) -> str: ...


class FileRepo(S3Storage):

    @abstractmethod
    async def _create_file_descr(self, obj): ...

    @abstractmethod
    def _get_file_size(self, file: BinaryIO) -> int: ...


class ImageRepo(S3Storage):

    @abstractmethod
    def _get_image_info(self, file: BinaryIO): ...
