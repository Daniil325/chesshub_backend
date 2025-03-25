from dataclasses import dataclass

from src.domain.article.entities import ArticleTag
from src.infra.database.sqla_repo import ArticleTagRepo


@dataclass(frozen=True)
class CreateArticleTagDto:
    tag_id: str
    article_id: str


@dataclass
class CreateArticleTagCommand:
    article_tag_repo: ArticleTagRepo

    async def __call__(self, dto: CreateArticleTagDto) -> tuple:
        article_tag = ArticleTag.create(dto.tag_id, dto.article_id)
        await self.article_tag_repo.create(article_tag)
        return (dto.tag_id, dto.article_id)
