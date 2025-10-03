from abc import ABC, abstractmethod
from typing import Any


class Repo(ABC):
    @abstractmethod
    async def insert(self, item: dict[str, Any]) -> None: ...

    @abstractmethod
    async def update(self, id: str | int, changes: dict[str, Any]) -> None: ...

    @abstractmethod
    async def delete(self, id: str | int) -> None: ...


class CategoryRepo(Repo): ...


class CommentRepo(Repo): ...


class UserReactionRepo(Repo): ...


class ArticleRepo(Repo): ...
