from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter
from pydantic import BaseModel

from src.application.article.article_reaction import (
    CreateArticleReactionCommand,
    CreateArticleReactionDto,
    UpdateArticleReactionCommand,
    UpdateArticleReactionDto,
    DeleteArticleReactionCommand,
    Reaction,
)
from src.presentation.base import ApiInputModelConfig

router = APIRouter(route_class=DishkaRoute)


class CreateArticleReaction(BaseModel):
    model_config = ApiInputModelConfig
    article_id: str
    reaction: int


class UpdateArticleReaction(BaseModel):
    model_config = ApiInputModelConfig
    id: str
    reaction: int


@router.post("/")
async def post_article_reaction(
    article_reaction: CreateArticleReaction,
    cmd: FromDishka[CreateArticleReactionCommand],
):
    identity = await cmd(
        CreateArticleReactionDto(
            article_id=article_reaction.article_id, reaction=article_reaction.reaction
        )
    )
    return identity


@router.patch("/{article_reaction_id}")
async def patch_article_reaction_id(
    id: str,
    article_reaction: UpdateArticleReaction,
    cmd: FromDishka[UpdateArticleReactionCommand],
):
    await cmd(UpdateArticleReactionDto(id=id, reaction=article_reaction.reaction))


@router.delete("/{article_reaction_id}")
async def delete_article_reaction(
    article_reaction_id: str, cmd: FromDishka[DeleteArticleReactionCommand]
):
    await cmd(article_reaction_id)
