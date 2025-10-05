from typing import AsyncIterable

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.repo import SQLCategoryRepo, SQLCommentRepo, SQLUserReactionRepo
from src.domain.protocols import CategoryRepo, CommentRepo, UserReactionRepo

from .session import DBSession


class DBSessionFactory(Provider):
    scope = Scope.REQUEST

    def __init__(self, settings):
        super().__init__()
        self.settings = settings

    @provide
    def get_db(self) -> DBSession:
        return DBSession(self.settings)

    @provide
    async def get_session(self, db: DBSession) -> AsyncIterable[AsyncSession]:
        async with db.sessionmaker() as session:
            yield session


class DBFactory(Provider):
    scope = Scope.REQUEST

    def __init__(self) -> None:
        super().__init__()

    @provide
    def get_category_repo(self, session: AsyncSession) -> CategoryRepo:
        return SQLCategoryRepo(session)

    @provide
    def get_comment_repo(self, session: AsyncSession) -> CommentRepo:
        return SQLCommentRepo(session)

    @provide
    def get_user_reaction_service(self, session: AsyncSession) -> UserReactionRepo:
        return SQLUserReactionRepo(session)
