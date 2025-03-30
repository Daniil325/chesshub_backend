from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.article.protocols import TagRepo
from src.infra.database.sqla_repo import SqlTagRepo


class SqlProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session = session

    @provide
    def get_content_repo(self) -> TagRepo:
        return SqlTagRepo(self.session)
