from dataclasses import dataclass
from typing import Any

from src.domain.article.entities import Article
from src.infra.database.sqla_repo import ArticleRepo


@dataclass(frozen=True)
class CreateArticleDto:
    content: dict[str, Any]
    author_id: str
    category_id: str
    preview: str | None = None


@dataclass
class CreateArticleCommand:
    article_repo: ArticleRepo

    async def __call__(self, dto: CreateArticleDto) -> str:
        identity = self.article_repo.new_id()
        article = Article.create(identity, **dto)
        await self.article_repo.add(article)
        return identity


@dataclass
class UpdateArticleDto:
    article_id: str
    content: dict[str, Any]
    category_id: str
    preview: str | None = None


@dataclass
class UpdateArticleCommand:
    article_repo: ArticleRepo

    async def __call__(self, dto: UpdateArticleDto) -> None:
        article = await self.article_repo.get(dto.article_id)
        article.content = dto.content
        await self.article_repo.update(dto.article_id, article)


@dataclass
class DeleteArticleCommand:
    article_repo: ArticleRepo

    async def __call__(self, article_id: str) -> str:
        await self.article_repo.delete(article_id)
        return article_id
