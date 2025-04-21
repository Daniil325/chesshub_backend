from dataclasses import dataclass
from typing import BinaryIO, ClassVar

from src.domain.exceptions import DomainError
from src.infra.protocols import S3Storage


@dataclass(frozen=True)
class CreateImageDto:
    filename: str
    content_type: str
    file: BinaryIO
    size: int


@dataclass
class CreateImageCommand:
    allowed_content_types: ClassVar[tuple[str]] = (
        "image/png",
        "image/gif",
        "image/jpeg",
    )
    storage: S3Storage

    async def __call__(self, dto: CreateImageDto) -> str:
        if dto.content_type not in self.allowed_content_types:
            raise DomainError(f'Bad image content type "{dto.content_type}"')
        return await self.storage.upload(dto.filename, dto.file, dto.size)
