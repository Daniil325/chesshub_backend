from dataclasses import dataclass

from src.domain.article.entities import ArticleReaction, Reaction
from src.domain.article.protocols import ArticleReactionRepo


@dataclass(frozen=True)
class CreateArticleReactionDto:
    article_id: str
    reaction: Reaction


@dataclass
class CreateArticleReactionCommand:
    article_reaction_repo: ArticleReactionRepo

    async def __call__(self, dto: CreateArticleReactionDto) -> str:
        identity = self.article_reaction_repo.new_id()
        article_reaction = ArticleReaction.create(
            identity, dto.article_id, dto.reaction
        )
        await self.article_reaction_repo.add(article_reaction)
        return identity


@dataclass
class UpdateArticleReactionDto:
    id: str
    reaction: Reaction


@dataclass
class UpdateArticleReactionCommand:
    article_reaction_repo: ArticleReactionRepo

    async def __call__(self, dto: UpdateArticleReactionDto):
        article_reaction = await self.article_reaction_repo.get(dto.id)
        article_reaction.reaction = dto.reaction

        await self.article_reaction_repo.update(dto.id, dto.reaction)


@dataclass
class DeleteArticleReactionCommand:
    article_reaction_repo: ArticleReactionRepo

    async def __call__(self, id: str) -> None:
        await self.article_reaction_repo.delete(id)
