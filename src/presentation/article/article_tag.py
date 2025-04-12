from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter
from pydantic import BaseModel

from src.application.article.article_tag import (
    CreateArticleTagCommand,
    CreateArticleTagDto,
)
from src.presentation.base import ApiInputModelConfig

router = APIRouter(route_class=DishkaRoute)


class CreateAricleTag(BaseModel):
    model_config = ApiInputModelConfig
    tag_id: str
    article_id: str


@router.post("/")
async def post_article_tag(
    article_tag: CreateAricleTag, cmd: FromDishka[CreateArticleTagCommand]
):
    identity = await cmd(
        CreateArticleTagDto(
            tag_id=article_tag.tag_id, article_id=article_tag.article_id
        )
    )
    return identity
