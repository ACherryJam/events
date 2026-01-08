from dishka import AsyncContainer, Scope

from events.domain.event import DomainEvent
from events.domain.event_handler import DomainEventHandler, DomainEventHandlerFactory


class DishkaDomainEventHandlerFactory(DomainEventHandlerFactory):
    def __init__(
        self,
        container: AsyncContainer
    ) -> None:
        self.container = container

    async def create[E: DomainEvent](
        self, 
        event_type: type[E]
    ) -> list[DomainEventHandler[E]]:
        handler_types = DomainEventHandler.registry.get(event_type)

        # async with self.container(scope=Scope.REQUEST) as container:
        return [
            await self.container.get(handler_type)
            for handler_type in handler_types
        ]
