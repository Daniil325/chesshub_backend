from abc import ABC, abstractmethod
from typing import Any

from src.domain.article.entities import (
    Tag,
    ArticleReaction,
    ArticleTag,
    Category,
    Reaction,
)


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


class ArticleReactionRepo(ABC):

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

    async def add(self, article_reaction: ArticleReaction) -> None: ...

    @abstractmethod
    async def get(self, article_reaction_id: str) -> ArticleReaction | None: ...

    @abstractmethod
    async def update(self, id: str, reaction: Reaction) -> None: ...

    @abstractmethod
    async def delete(self, id: str) -> None: ...


class ArticleTagRepo(ABC):

    @abstractmethod
    def new_id(self) -> str: ...

    @abstractmethod
    async def add(self, article_tag: ArticleTag) -> None: ...

    @abstractmethod
    async def get(self, article_tag_keys: dict) -> ArticleTag | None: ...

    @abstractmethod
    async def update(self, article_tag_keys: ArticleTag) -> None: ...

    @abstractmethod
    async def delete(self, tag_id: str, article_id: str) -> None: ...


class CategoryRepo(ABC):

    @abstractmethod
    def new_id(self) -> str: ...

    @abstractmethod
    async def add(self, category: Category) -> None: ...

    @abstractmethod
    async def get(self, category_id: str) -> Category | None: ...

    @abstractmethod
    async def update(self, category_id: str, changes: dict[str, Any]) -> None: ...

    @abstractmethod
    async def delete(self, category_id: str) -> None: ...


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