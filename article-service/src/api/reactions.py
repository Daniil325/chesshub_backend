from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter
from pydantic import BaseModel

from src.application.crud_service import UserReactionService

from .base import ApiInputModelConfig, ModelResponse


class UserReactionResponse(BaseModel):
    user_id: str
    article_id: str
    reaction_type: str


class CreateUserReaction(UserReactionResponse):
    model_config = ApiInputModelConfig


router = APIRouter(route_class=DishkaRoute)

UserReactionModelResponse = ModelResponse[UserReactionResponse]


@router.post("/", response_model=UserReactionModelResponse)
async def post_reaction(
    reaction: CreateUserReaction, service: FromDishka[UserReactionService]
):
    result = await service.create(reaction)
    return {"item": result}


@router.patch(
    "/{article_id}/{user_id}", response_model=UserReactionModelResponse
)
async def update_reaction(
    reaction: CreateUserReaction,
    service: FromDishka[UserReactionService],
    user_id: str,
    article_id: str,
):
    result = await service.update(user_id, article_id)
    return {"item": result}


@router.delete(
    "/{article_id}/{user_id}", response_model=UserReactionModelResponse
)
async def delete_reaction(
    reaction: CreateUserReaction,
    service: FromDishka[UserReactionService],
    user_id: str,
    article_id: str,
):
    return await service.delete(user_id, article_id)
