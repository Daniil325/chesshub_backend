from typing import Any
from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.article.entities import Article
from src.domain.user.entities import User
from src.domain.user.protocols import UserRepo
from src.infra.database.sqla_repo import SqlHelper


class SqlUserRepo(SqlHelper, UserRepo):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def register(self, user: User):
        await self.add(user)

    async def login_by_username(self, username: str, password: str):
        stmt = select(User).where(and_(User.username == username, User.password == password))
        user = (await self.session.execute(stmt)).scalar_one_or_none()
        return user

    async def get_user_articles(self, username: str) -> list[Article]:
        user = await self.get_user_by_username(username)
        user_id = user.id
        stmt = select(Article, User).join(User).where(Article.author_id == user_id)
        items = (await self.session.execute(stmt)).all()
        return items

    async def change_profile(self, id: UUID, changes: dict[str, Any]) -> None:
        await self.update(id, changes)

    async def get_user_by_username(self, username: str) -> User:
        stmt = select(User).where(User.username == username)
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        return result
