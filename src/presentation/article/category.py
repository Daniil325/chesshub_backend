from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter
from pydantic import BaseModel

from src.application.article.category import (
    CreateCategoryCommand,
    CreateCategoryDto,
    UpdateCategoryCommand,
    UpdateCategoryDto,
    DeleteCategoryCommand,
)
from src.presentation.base import ApiInputModelConfig

router = APIRouter(route_class=DishkaRoute)


class CreateCategory(BaseModel):
    model_config = ApiInputModelConfig
    name: str


class UpdateCategory(BaseModel):
    model_config = ApiInputModelConfig
    name: str


@router.post("/")
async def post_category(
    category: CreateCategory,
    cmd: FromDishka[CreateCategoryCommand],
):
    identity = await cmd(CreateCategoryDto(name=category.name))
    return identity


@router.patch("/{id}")
async def patch_category(
    id: str, category: UpdateCategory, cmd: FromDishka[UpdateCategoryCommand]
):
    await cmd(UpdateCategoryDto(category_id=id, name=category.name))


@router.delete("/")
async def delete_tag(tag_id: str, cmd: FromDishka[DeleteCategoryCommand]):
    await cmd(tag_id)
