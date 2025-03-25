from dataclasses import dataclass

from src.domain.article.entities import ArticleReaction
from src.infra.database.sqla_repo import ArticalReactionRepo
from src.domain.article.entities import Reaction


@dataclass(frozen=True)
class CreateArticleReactionDto:
    article_id: str
    reaction: Reaction

@dataclass
class CreateArticalReactionCommand:
    artical_reaction_repo: ArticalReactionRepo

    async def __call__(self, dto: CreateArticleReactionDto) -> str:
        identity = self.artical_reaction_repo.new_id()
        artical_reaction = ArticleReaction.create(identity, dto.article_id, dto.reaction)
        await self.artical_reaction_repo.create(artical_reaction)
        return identity
