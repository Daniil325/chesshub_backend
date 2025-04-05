from abc import ABC, abstractmethod
from typing import Any

from src.domain.article.entities import Article, Tag


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


class ArticleRepo(ABC):

    @abstractmethod
    def new_id(self) -> str: ...

    @abstractmethod
    async def add(self, article: Article) -> None: ...

    @abstractmethod
    async def get(self, article_id: str) -> Article | None: ...

    @abstractmethod
    async def update(self, article_id: str, changes: dict[str, Any]) -> None: ...

    @abstractmethod
    async def delete(self, article_id: str) -> None: ...

    @abstractmethod
    async def get_by_category(self, category_id: str) -> list[Article]: ...

    @abstractmethod
    async def get_by_author(self, author_id: str) -> list[Article]: ...
