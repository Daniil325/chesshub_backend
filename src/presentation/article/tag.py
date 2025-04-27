from typing import Annotated, Literal
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path, Query
from pydantic import BaseModel, Field

from src.application.article.tag import (
    CreateTagCommand,
    CreateTagDto,
    DeleteTagCommand,
    UpdateTagCommand,
    UpdateTagDto,
)
from src.infra.database.reader import TagReader
from src.presentation.base import (
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
    order_by: Literal["name", "-name"] = "name"
    filter: str = ""


class TagResponse(BaseModel):
    id: UUID
    name: str


@router.get("/", response_model=PaginatedListResponse[TagResponse])
async def get_list_categories(
    filter_query: Annotated[FilterParams, Query()], reader: FromDishka[TagReader]
):
    items = await reader.fetch_list(
        filter_query.offset,
        filter_query.limit,
        filter_query.filter,
        filter_query.order_by,
    )
    return {
        "items": items,
        "page": filter_query.offset + 1,
        "per_page": filter_query.limit,
    }


@router.get("/{id}", response_model=ModelResponse[TagResponse])
async def get_article(reader: FromDishka[TagReader], id: str = Path()):
    item = check_found(await reader.fetch_by_id(id))
    return {"item": item}


class CreateTag(BaseModel):
    model_config = ApiInputModelConfig
    name: str


class UpdateTag(BaseModel):
    model_config = ApiInputModelConfig
    name: str


@router.post("/")
async def post_tag(tag: CreateTag, cmd: FromDishka[CreateTagCommand]):
    identity = await cmd(CreateTagDto(name=tag.name))
    return identity


@router.patch("/{id}", response_model=SuccessResponse)
async def patch_tag(
    tag: UpdateTag, cmd: FromDishka[UpdateTagCommand], id: str
):
    await cmd(UpdateTagDto(tag_id=id, name=tag.name))
    return SuccessResponse()


@router.delete("/{id}", response_model=SuccessResponse)
async def delete_tag(cmd: FromDishka[DeleteTagCommand], id: str):
    await cmd(id)
    return SuccessResponse()
