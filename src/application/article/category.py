from dataclasses import asdict, dataclass

from src.domain.article.entities import Category
from src.domain.article.protocols import CategoryRepo


@dataclass(frozen=True)
class CreateCategoryDto:
    name: str


@dataclass
class CreateCategoryCommand:
    category_repo: CategoryRepo

    async def __call__(self, dto: CreateCategoryDto) -> str:
        identity = self.category_repo.new_id()
        category = Category.create(identity, dto.name)
        await self.category_repo.add(category)
        return identity


@dataclass(frozen=True)
class UpdateCategoryDto:
    category_id: str
    name: str


@dataclass
class UpdateCategoryCommand:
    category_repo: CategoryRepo

    async def __call__(self, dto: UpdateCategoryDto) -> str:
        category = await self.category_repo.get(dto.category_id)
        category.name = dto.name
        await self.category_repo.update(dto.category_id, asdict(category))


@dataclass
class DeleteCategoryCommand:
    category_repo: CategoryRepo

    async def __call__(self, content_id: str) -> None:
        await self.category_repo.delete(content_id)
        return content_id
