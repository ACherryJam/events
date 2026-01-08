from events.domain.event_handler import DomainEventHandler

from common.contracts.user import UserRegisteredV1

from user_service.domain.user.events import UserRegistered
from user_service.infrastructure.outbox.outbox import Outbox 


class UserRegisteredEventHandler(DomainEventHandler[UserRegistered]):
    def __init__(
        self,
        outbox: Outbox
    ) -> None:
        self.outbox = outbox

    async def handle(self, event: UserRegistered) -> None:
        await self.outbox.put(UserRegisteredV1(event.user.email))
