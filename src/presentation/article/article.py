from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path, Query
from pydantic import BaseModel, Field, Json

from src.application.article.image import CreateImageCommand
from src.application.article.article import (
    CommentDto,
    CreateArticleCommand,
    CreateArticleDto,
    DeleteArticleCommand,
    PostCommentCommand,
    UpdateArticleCommand,
    UpdateArticleDto,
)
from src.infra.database.reader import ArticleReader
from src.presentation.base import (
    APIModelConfig,
    ApiInputModelConfig,
    ModelResponse,
    PaginatedListResponse,
    SuccessResponse,
    check_found,
)

router = APIRouter(route_class=DishkaRoute)


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["pub_date", "-pub_date", "views", "-views"] = "pub_date"
    filter: str = ""


class ArticleResponse(BaseModel):
    id: UUID
    title: str
    content: dict[str, Any]
    category_id: str
    preview: str | None = None
    pub_date: datetime
    views: int = 0
    category_id: UUID
    category_name: str
    username: str
    model_config = APIModelConfig


@router.get("/", response_model=PaginatedListResponse[ArticleResponse])
async def get_articles_list(
    filter_query: Annotated[FilterParams, Query()], reader: FromDishka[ArticleReader]
):
    result = await reader.fetch_list(
        filter_query.offset,
        filter_query.limit,
        filter_query.filter,
        filter_query.order_by,
    )
    return {
        "items": result,
        "page": filter_query.offset + 1,
        "per_page": filter_query.limit,
    }


ArticleModelResponse = ModelResponse[ArticleResponse]


@router.get("/{id}", response_model=ArticleModelResponse)
async def get_article(reader: FromDishka[ArticleReader], id: str = Path()):
    item = check_found(await reader.fetch_by_id(id))
    return {"item": item}


class CreateArticle(BaseModel):
    model_config = ApiInputModelConfig
    title: str
    content: dict[str, Any]
    category_id: str
    author_id: str
    preview: str | None = None


@router.post("/", response_model=SuccessResponse)
async def post_article(article: CreateArticle, cmd: FromDishka[CreateArticleCommand]):
    identity = await cmd(
        CreateArticleDto(
            article.title,
            article.content,
            UUID("29abbf0a-f14a-47ff-93d4-ca05d79283c5"),
            article.author_id,
            article.preview,
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
    return SuccessResponse()


@router.delete("/{id}", response_model=SuccessResponse)
async def delete_article(cmd: FromDishka[DeleteArticleCommand], id: UUID = Path(...)):
    await cmd(id)
    return SuccessResponse()


class PostComment(BaseModel):
    author_id: str
    article_id: str
    text: str


@router.post("/comment/{id}", response_model=SuccessResponse)
async def post_comment(cmd: FromDishka[PostCommentCommand], comment: PostComment, id: UUID = Path(...), ):
    identity = await cmd(CommentDto(comment.article_id, comment.author_id, comment.text))
    return identity