import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from user_service.domain.user.entity import User, UserId
from user_service.domain.user.repository import UserRepository
from user_service.infrastructure.persistence.models.user.model import UserModel
from user_service.infrastructure.persistence.models.user.mapper import UserMapper


class SQLUserRepository(UserRepository):
    def __init__(
        self,
        session: AsyncSession
    ):
        self.session = session

    async def get_next_id(self) -> UserId:
        return UserId(value=uuid.uuid4())

    async def get_by_id(self, id: UserId) -> User:
        model = await self.session.get(UserModel, str(id.value))
        if model is None:
            raise Exception(f"User with id {id.value} is not found")
        
        return await UserMapper.to_domain(model)

    async def insert(self, user: User) -> None:
        model = await UserMapper.from_domain(user)
        self.session.add(model)

    async def update(self, user: User) -> None:
        model = await self.session.get(UserModel, str(user.id.value))
        if model is None:
            raise Exception(f"User with id {user.id.value} is not found")

        new_model = await UserMapper.from_domain(user)
        model.email = new_model.email
        model.password = new_model.password

        self.session.add(model)

    async def delete(self, user: User) -> None:
        model = await self.session.get(UserModel, str(user.id.value))
        if model is None:
            raise Exception(f"User with id {user.id.value} is not found")

        await self.session.delete(model)
    