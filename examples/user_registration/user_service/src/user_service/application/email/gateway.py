import abc
from typing import Protocol

from user_service.domain.user.entity import User


class EmailGateway(Protocol):
    @abc.abstractmethod
    async def send_confirmation(self, user: User) -> None:
        ...
    