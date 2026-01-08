from dataclasses import dataclass
from events.integration.event import IntegrationEvent

from .topic import _user_service


@dataclass
class UserRegisteredV1(IntegrationEvent):
    type = f"{_user_service}.user_registered"
    version = 1

    email: str
