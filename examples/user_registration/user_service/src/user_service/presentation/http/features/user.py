from typing import Annotated
from fastapi import Body
from fastapi.routing import APIRouter
from dishka.integrations.fastapi import inject, FromDishka
from pydantic import BaseModel

from user_service.application.user.register_user import RegisterUserInteractor

user_router = APIRouter(prefix="/user")


class UserDTO(BaseModel):
    email: str
    password: str


@user_router.post("/register")
@inject
async def register(
    user: Annotated[UserDTO, Body()],
    interactor: FromDishka[RegisterUserInteractor]
):
    await interactor(user.email, user.password)
