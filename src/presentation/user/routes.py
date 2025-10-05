from dataclasses import asdict
from typing import Annotated, Any, Literal

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from src.application.user.usecases import (
    LoginCommand,
    LoginDto,
    ProfileDto,
    RegisterCommand,
    RegisterUserDto,
    UpdateProfileCommand,
)
from src.infra.database.reader import UserReader
from src.presentation.base import SuccessResponse

router = APIRouter(route_class=DishkaRoute)


class RegisterUser(BaseModel):
    name: str
    surname: str
    username: str
    password: str
    email: str


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["username"] = "username"
    filter: str = ""


@router.get("/")
async def get_users_list(
    filter_query: Annotated[FilterParams, Query()], reader: FromDishka[UserReader]
):
    items = await reader.fetch_list(
        filter_query.offset,
        filter_query.limit,
        filter_query.filter,
        filter_query.order_by,
    )
    return {"items": items}


@router.post("/register")
async def register_user(user: RegisterUser, cmd: FromDishka[RegisterCommand]):
    identity = await cmd(
        RegisterUserDto(
            user.name, user.surname, user.username, user.password, user.email
        )
    )
    return asdict(identity)


class LoginUser(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(user: LoginUser, cmd: FromDishka[LoginCommand]):
    user = await cmd(LoginDto(user.username, user.password))
    return user


@router.get("/profile/{username}")
async def get_profile(username: str, reader: FromDishka[UserReader]):
    user = await reader.get_by_username(username)
    return user


class UserProfile(BaseModel):
    username: str
    name: str
    surname: str
    password: str
    email: str
    user_info: dict[str, Any]


@router.patch("/profile/{username}", response_model=SuccessResponse)
async def update_profile(
    username: str, changes: UserProfile, cmd: FromDishka[UpdateProfileCommand]
):
    result = await cmd(
        ProfileDto(
            changes.username,
            changes.name,
            changes.surname,
            changes.password,
            changes.email,
            changes.user_info,
        )
    )
    return SuccessResponse()
