from pydantic import BaseModel

from src.domain.entities import Category, Comment, UserReaction
from src.domain.base import Entity
from src.infra.protocols import AbstractRepository


class CRUDService:
    entity: Entity
    repo: AbstractRepository

    def __init__(self, entity: Entity, repo: AbstractRepository):
        self.entity = entity
        self.repo = repo

    async def create(self, item: BaseModel) -> Entity:
        db_item: Entity = self.entity.create(**item.model_dump())
        await self.repo.insert(db_item)
        return db_item

    async def update(self, id: str | int, changes: BaseModel) -> str | int:
        await self.repo.update(id, changes.model_dump())
        return id

    async def delete(self, id: str | int) -> str | int:
        await self.repo.delete(id)
        return id


class CategoryService(CRUDService):

    def __init__(self, repo):
        super().__init__(Category, repo)


class CommentService(CRUDService):
    def __init__(self, repo):
        super().__init__(Comment, repo)


class UserReactionService(CRUDService):

    def __init__(self, repo):
        super().__init__(UserReaction, repo)
