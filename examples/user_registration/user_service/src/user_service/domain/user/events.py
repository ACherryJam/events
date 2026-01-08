from typing import TYPE_CHECKING
from dataclasses import dataclass
from events.domain.event import DomainEvent

if TYPE_CHECKING:
    from user_service.domain.user.entity import User


@dataclass
class UserRegistered(DomainEvent):
    user: "User"
    type: str = "user.user_registered" # type: ignore
