from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter
from pydantic import BaseModel

from src.application.article.article_tag import (
    CreateArticleTagCommand,
    CreateArticleTagDto,
    UpdateArticleTagCommand,
    UpdateArticleTagDto,
    DeleteArticleTagCommand,
)
from src.presentation.base import ApiInputModelConfig

router = APIRouter(route_class=DishkaRoute)


class CreateAricleTag(BaseModel):
    model_config = ApiInputModelConfig
    tag_id: str
    article_id: str


class UpdateArticleTag(BaseModel):
    model_config = ApiInputModelConfig
    old_tag_id: str
    old_article_id: str
    new_tag_id: str
    new_article_id: str


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


@router.patch("/{tag_id}/{article_id}")
async def patch_article_tag(
    article_tag: UpdateArticleTag, cmd: FromDishka[UpdateArticleTagCommand]
):
    await cmd(
        UpdateArticleTagDto(
            old_article_id=article_tag.old_article_id,
            old_tag_id=article_tag.old_tag_id,
            new_tag_id=article_tag.new_tag_id,
            new_article_id=article_tag.new_article_id,
        )
    )


@router.delete("/{tag_id}/{article_id}")
async def delete_article_tag(
    tag_id: str, article_id: str, cmd: FromDishka[DeleteArticleTagCommand]
):
    await cmd(tag_id=tag_id, article_id=article_id)
