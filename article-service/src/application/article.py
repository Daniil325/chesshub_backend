from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any

from src.infra.database.mapping import ArticleInDb
from src.domain.entities import Article
from src.domain.exceptions import DomainError
from src.infra.protocols import ImageRepo
from src.domain.protocols import ArticleRepo


@dataclass
class BaseArticleCommand:
    article_repo: ArticleRepo
    storage_repo: ImageRepo

    async def check_image(self, image_id: str | None):
        if image_id is None:
            return
        if not await self.storage_repo.exists(image_id):
            raise DomainError(f"Image {image_id} does not exist")


@dataclass(frozen=True)
class ArticleDto:
    title: str
    content: dict[str, Any]
    user_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    views: int = 0
    preview: str | None = None


@dataclass
class CreateArticleCommand(BaseArticleCommand):

    async def __call__(self, dto: ArticleDto) -> str:
        await self.check_image(dto.preview)
        article = Article.create(**asdict(dto))
        article_in_db = ArticleInDb(**asdict(article))
        await self.article_repo.add(article_in_db)
        return article.id


@dataclass
class UpdateArticleCommand(BaseArticleCommand):

    async def __call__(self, dto: ArticleDto, article_id: str) -> str:
        article = await self.article_repo.get(dto.article_id)
        await self.check_image(dto.preview)
        await self.article_repo.update(article_id, asdict(article))
        return article_id


@dataclass
class DeleteArticleCommand:
    article_repo: ArticleRepo

    async def __call__(self, id: str) -> str:
        await self.article_repo.delete(id)
        return id
