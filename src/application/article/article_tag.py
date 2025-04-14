from dataclasses import asdict, dataclass

from src.domain.article.entities import ArticleTag
from src.domain.article.protocols import ArticleTagRepo


@dataclass(frozen=True)
class CreateArticleTagDto:
    tag_id: str
    article_id: str


@dataclass
class CreateArticleTagCommand:
    article_tag_repo: ArticleTagRepo

    async def __call__(self, dto: CreateArticleTagDto) -> dict:
        article_tag = ArticleTag.create(dto.tag_id, dto.article_id)
        await self.article_tag_repo.add(article_tag)
        return [dto.tag_id, dto.article_id]


@dataclass(frozen=True)
class UpdateArticleTagDto:
    old_tag_id: str
    old_article_id: str
    new_tag_id: str
    new_article_id: str


@dataclass
class UpdateArticleTagCommand:
    article_tag_repo: ArticleTagRepo

    async def __call__(self, dto: UpdateArticleTagDto) -> dict:
        await self.article_tag_repo.delete(dto.old_tag_id, dto.old_article_id)
        new_article_tag = ArticleTag.create(dto.new_tag_id, dto.new_article_id)
        await self.article_tag_repo.add(new_article_tag)
        return [dto.new_tag_id, dto.new_article_id]


@dataclass
class DeleteArticleTagCommand:
    article_tag_repo: ArticleTagRepo

    async def __call__(self, tag_id: str, article_id: str) -> None:
        await self.article_tag_repo.delete(tag_id, article_id)
        return [tag_id, article_id]
