from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.session import DBSession
from src.domain.article.protocols import (
    ArticleRepo,
    CategoryRepo,
    TagRepo,
    ArticleTagRepo,
)
from src.infra.database.sqla_repo import (
    SqlArticleRepo,
    SqlCategoryRepo,
    SqlTagRepo,
    SqlArticleTagRepo,
)


class DBSessionProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self, settings):
        super().__init__()
        self.settings = settings

    @provide
    def get_db(self) -> DBSession:
        return DBSession(self.settings)

    @provide
    async def get_session(self, db: DBSession) -> AsyncSession:
        return await db.get_session()


class SqlProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self) -> None:
        super().__init__()

    @provide
    def get_content_repo(self, session: AsyncSession) -> TagRepo:
        return SqlTagRepo(session)

    @provide
    def get_article_repo(self, session: AsyncSession) -> ArticleRepo:
        return SqlArticleRepo(session)

    @provide
    def get_category_repo(self, session: AsyncSession) -> CategoryRepo:
        return SqlCategoryRepo(session)

    @provide
    def get_article_tag_repo(self, session: AsyncSession) -> ArticleTagRepo:
        return SqlArticleTagRepo(session)
