import uuid
from events.domain.aggregate import AggregateRoot

from user_service.domain.user.events import UserRegistered


class UserId:
    def __init__(self, value: uuid.UUID):
        self.value = value


class User(AggregateRoot):
    def __init__(
        self,
        id: UserId,
        email: str,
        password: str
    ) -> None:
        super().__init__()

        self.id = id
        self.email = email
        self.password = password  # Hmmm, I wonder if that's safe!

    def initialize(self):
        self.publish_event(UserRegistered(self))
    