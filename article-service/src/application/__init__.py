from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.repo import SQLCategoryRepo
from src.application.crud_service import (
    CategoryService,
    CommentService,
    UserReactionService,
)


class ServiceFactory(Provider):
    scope = Scope.REQUEST

    def __init__(self):
        super().__init__()

    @provide
    def get_category_service(self, session: AsyncSession) -> CategoryService:
        return CategoryService(SQLCategoryRepo(session))

    @provide
    def get_comment_service(self) -> CommentService:
        return CommentService(CommentRepo)

    @provide
    def get_user_reaction_service(self) -> UserReactionService:
        return UserReactionService(UserReactionService)
