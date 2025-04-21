from typing import Any
from uuid import UUID
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Path
from pydantic import BaseModel, Json

from src.application.article.article import (
    CreateArticleCommand,
    CreateArticleDto,
    DeleteArticleCommand,
    UpdateArticleCommand,
    UpdateArticleDto,
)
from src.presentation.base import ApiInputModelConfig, SuccessResponse


router = APIRouter(route_class=DishkaRoute)


class CreateArticle(BaseModel):
    model_config = ApiInputModelConfig
    title: str
    content: dict[str, Any]
    category_id: str
    preview: str | None = None


@router.post("/", response_model=SuccessResponse)
async def post_article(article: CreateArticle, cmd: FromDishka[CreateArticleCommand]):
    identity = await cmd(
        CreateArticleDto(
            article.title, article.content, article.category_id, article.preview
        )
    )
    return identity


class UpdateArticle(BaseModel):
    model_config = ApiInputModelConfig
    title: str
    content: Json
    category_id: str
    preview: str | None = None


@router.patch("/{id}", response_model=SuccessResponse)
async def update_article(
    article: UpdateArticle, cmd: FromDishka[UpdateArticleCommand], id: UUID = Path(...)
):
    await cmd(UpdateArticleDto(article_id=id, **article))


@router.delete("/{id}", response_model=SuccessResponse)
async def delete_article(cmd: FromDishka[DeleteArticleCommand], id: UUID = Path(...)):
    await cmd(id)
