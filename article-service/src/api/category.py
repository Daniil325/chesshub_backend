from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path
from pydantic import BaseModel

from src.application.crud_service import CategoryService

from .base import ApiInputModelConfig, ModelResponse


class CategoryResponse(BaseModel):
    id: str
    name: str


class CreateCategory(BaseModel):
    model_config = ApiInputModelConfig
    name: str


router = APIRouter(route_class=DishkaRoute)

CategoryModelResponse = ModelResponse[CategoryResponse]


@router.post("/", response_model=CategoryModelResponse)
async def post_category(category: CreateCategory, service: FromDishka[CategoryService]):
    result = await service.create(category)
    return {"item": result}


@router.patch("/{id}", response_model=CategoryModelResponse)
async def update_category(
    category: CreateCategory,
    service: FromDishka[CategoryService],
    id: str = Path(...),
):
    result = await service.update(id, category)
    return {"item": result}


@router.delete("/{id}")
async def delete_category(service: FromDishka[CategoryService], id: str = Path(...)):
    return await service.delete(id)
