from dataclasses import asdict, dataclass
from typing import Any

from src.domain.article.protocols import ArticleRepo, CommentRepo
from src.domain.exceptions import DomainError
from src.domain.article.entities import Article, Comment
from src.infra.protocols import S3Storage


@dataclass
class BaseArticleCommand:
    article_repo: ArticleRepo
    storage_repo: S3Storage

    async def check_image(self, image_id: str | None):
        if image_id is None:
            return
        if not await self.storage_repo.exists(image_id):
            raise DomainError(f"Image {image_id} does not exist")


@dataclass(frozen=True)
class CreateArticleDto:
    title: str
    content: dict[str, Any]
    category_id: str
    author_id: str
    preview: str | None = None


@dataclass
class CreateArticleCommand(BaseArticleCommand):
    async def __call__(self, dto: CreateArticleDto) -> str:
        identity = self.article_repo.new_id()
        await self.check_image(dto.preview)
        article = Article.create(
            identity,
            dto.title,
            dto.content,
            dto.category_id,
            dto.author_id,
            dto.preview,
        )
        await self.article_repo.add(article)
        return identity


@dataclass
class UpdateArticleDto:
    article_id: str
    title: str
    content: dict[str, Any]
    category_id: str
    preview: str | None = None


@dataclass
class UpdateArticleCommand(BaseArticleCommand):

    async def __call__(self, dto: UpdateArticleDto) -> None:
        article = await self.article_repo.get(dto.article_id)
        await self.check_image(dto.preview)
        article.content = dto.content
        article.title = dto.title
        article.preview = dto.preview
        await self.article_repo.update(dto.article_id, article)


@dataclass
class DeleteArticleCommand:
    article_repo: ArticleRepo

    async def __call__(self, article_id: str) -> str:
        await self.article_repo.delete(article_id)
        return article_id
    
    
@dataclass
class CommentDto:
    article_id: str
    author_id: str
    text: str
    
    
@dataclass
class PostCommentCommand:
    comment_repo: CommentRepo
    
    async def __call__(self, dto: CommentDto):
        identity = self.comment_repo.new_id()
        comment = Comment.create(identity, **asdict(dto))
        await self.comment_repo.post_comment(comment)
        return identity
