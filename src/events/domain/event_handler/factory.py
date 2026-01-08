from typing import Protocol

from events.domain.event import DomainEvent

from .handler import DomainEventHandler


class DomainEventHandlerFactory(Protocol):
    async def create[E: DomainEvent](
        self,
        event_type: type[E]
    ) -> list[DomainEventHandler[E]]:
        ...
