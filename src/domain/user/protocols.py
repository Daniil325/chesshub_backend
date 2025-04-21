from abc import ABC, abstractmethod

from src.domain.article.entities import Article
from .entities import User


class UserRepo(ABC):

    @abstractmethod
    async def register(self, user: User) -> None: ...

    @abstractmethod
    async def login_by_username(self, username: str, password: str) -> User: ...

    @abstractmethod
    async def get_user_articles(self, username: str) -> list[Article]: ...

    @abstractmethod
    async def change_profile(self, user: User) -> None: ...

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User: ...
