from dataclasses import dataclass

from src.domain.article.entities import Category
from src.infra.database.sqla_repo import CategoryRepo


@dataclass(frozen=True)
class CreateCategoryDto:
    name: str


@dataclass
class CreateCategoryCommand:
    category_repo: CategoryRepo

    async def __call__(self, dto: CreateCategoryDto) -> str:
        identity = self.category_repo.new_id()
        category = Category.create(identity, dto.name)
        await self.category_repo.create(category)
        return identity
