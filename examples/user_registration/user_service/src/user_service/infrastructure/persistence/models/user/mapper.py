

import uuid
from user_service.domain.user.entity import User, UserId
from user_service.infrastructure.persistence.models.user.model import UserModel


class UserMapper:
    @staticmethod
    async def from_domain(user: User) -> UserModel:
        return UserModel(
            id=str(user.id.value),
            email=user.email,
            password=user.password
        )

    @staticmethod
    async def to_domain(model: UserModel) -> User:
        return User(
            id=UserId(uuid.UUID(model.id)),
            email=model.email,
            password=model.password
        )
