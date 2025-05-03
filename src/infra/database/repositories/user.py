from sqlalchemy import select
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

    async def login_by_username(self, username: str, password: str): ...

    async def get_user_articles(self, username: str) -> list[Article]: ...

    async def change_profile(self, user: User) -> None: ...

    async def get_user_by_username(self, username: str) -> User:
        stmt = select(User).where(User.username == username)
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        return result
