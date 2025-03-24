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

    async def __call__(self, dto: CreateArticleTagDto) -> str:
        tag_id = self.article_tag_repo.new_id()
        article_id = self.article_tag_repo.new_id()
        article_tag = ArticleTag.create(tag_id, article_id)
        await self.article_tag_repo.create(article_tag)
        return tag_id
