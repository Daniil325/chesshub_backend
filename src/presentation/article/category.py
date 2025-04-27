from typing import Annotated, Literal
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path, Query
from pydantic import BaseModel, Field

from src.application.article.category import (
    CreateCategoryCommand,
    CreateCategoryDto,
    DeleteCategoryCommand,
    UpdateCategoryCommand,
    UpdateCategoryDto,
)
from src.infra.database.reader import CategoryReader
from src.presentation.base import ApiInputModelConfig, ModelResponse, PaginatedListResponse, SuccessResponse, check_found

router = APIRouter(route_class=DishkaRoute)


class CreateCategory(BaseModel):
    model_config = ApiInputModelConfig
    name: str


class UpdateCategory(BaseModel):
    model_config = ApiInputModelConfig
    name: str


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["name", "-name"] = "name"
    filter: str = ""
    
    
class CategoryResponse(BaseModel):
    id: UUID
    name: str


@router.get("/", response_model=PaginatedListResponse[CategoryResponse])
async def get_list_categories(
    filter_query: Annotated[FilterParams, Query()], reader: FromDishka[CategoryReader]
):
    items = await reader.fetch_list(
        filter_query.offset,
        filter_query.limit,
        filter_query.filter,
        filter_query.order_by,
    )
    return {"items": items, "page": filter_query.offset + 1, "per_page": filter_query.limit}


@router.get("/{id}", response_model=ModelResponse[CategoryResponse])
async def get_article(reader: FromDishka[CategoryReader], id: str = Path()):
    item = check_found(await reader.fetch_by_id(id))
    return {"item": item}


@router.post("/")
async def post_category(
    category: CreateCategory,
    cmd: FromDishka[CreateCategoryCommand],
):
    identity = await cmd(CreateCategoryDto(name=category.name))
    return identity


@router.patch("/{id}", response_model=SuccessResponse)
async def patch_category(
    id: str, category: UpdateCategory, cmd: FromDishka[UpdateCategoryCommand]
):
    await cmd(UpdateCategoryDto(category_id=id, name=category.name))
    return SuccessResponse()


@router.delete("/{id}", response_model=SuccessResponse)
async def delete_tag(tag_id: str, cmd: FromDishka[DeleteCategoryCommand]):
    await cmd(tag_id)
    return SuccessResponse()