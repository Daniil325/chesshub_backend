from dataclasses import asdict
from typing import Annotated, Any, Literal
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path, Query
from pydantic import BaseModel, Field, Json

from src.application.user.usecases import RegisterCommand, RegisterUserDto


router = APIRouter(route_class=DishkaRoute)


class RegisterUser(BaseModel):
    name: str
    surname: str
    username: str
    password: str
    email: str


@router.post("/register")
async def register_user(user: RegisterUser, cmd: FromDishka[RegisterCommand]):
    identity = await cmd(
        RegisterUserDto(user.name, user.surname, user.username, user.password, user.email)
    )
    return asdict(identity)


@router.get("/profile/{username}")
async def get_profile(reader: FromDishka[]):
    ...