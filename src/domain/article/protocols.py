from abc import ABC, abstractmethod
from typing import Any

from src.domain.article.entities import Tag


class TagRepo(ABC):

    @abstractmethod
    def new_id(self) -> str: ...

    @abstractmethod
    async def add(self, tag: Tag) -> None: ...

    @abstractmethod
    async def get(self, tag_id: str) -> Tag | None: ...

    @abstractmethod
    async def update(self, tag_id: str, changes: dict[str, Any]) -> None: ...

    @abstractmethod
    async def delete(self, tag_id: str) -> None: ...
