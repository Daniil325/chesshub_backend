from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path
from pydantic import BaseModel

from src.application.crud_service import CommentService

from .base import ApiInputModelConfig, ModelResponse


class CommentResponse(BaseModel):
    id: int
    user_id: str
    article_id: str
    text: str


class CreateComment(CommentResponse):
    model_config = ApiInputModelConfig


router = APIRouter(route_class=DishkaRoute)

CommentModelResponce = ModelResponse[CommentResponse]


@router.post("/", response_model=CommentModelResponce)
async def post_category(
    comment: CreateComment, service: FromDishka[CommentService]
):
    result = await service.create(comment)
    return {"item": result}


@router.patch("/{id}", response_model=CommentModelResponce)
async def update_category(
    category: CreateComment,
    service: FromDishka[CommentService],
    id: str = Path(...),
):
    result = await service.update(id, category)
    return {"item": result}


@router.delete("/{id}")
async def delete_comment(
    service: FromDishka[CommentService], id: str = Path(...)
):
    return await service.delete(id)
