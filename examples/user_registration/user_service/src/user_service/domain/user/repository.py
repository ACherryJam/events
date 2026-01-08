import abc

from user_service.domain.user.entity import User, UserId


class UserRepository(abc.ABC):
    @abc.abstractmethod
    async def get_next_id(self) -> UserId:
        ...

    @abc.abstractmethod
    async def get_by_id(self, id: UserId) -> User:
        ...

    @abc.abstractmethod
    async def insert(self, user: User) -> None:
        ...
    
    @abc.abstractmethod
    async def update(self, user: User) -> None:
        ...
    
    @abc.abstractmethod
    async def delete(self, user: User) -> None:
        ...
