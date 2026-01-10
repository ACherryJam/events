from dishka import AsyncContainer

from events.domain.event import DomainEvent
from events.domain.event_handler import DomainEventHandler, DomainEventHandlerFactory
from events.domain.event_handler.handler import DomainEventHandlerRegistry


class DishkaDomainEventHandlerFactory(DomainEventHandlerFactory):
    def __init__(
        self,
        container: AsyncContainer,
        registry: DomainEventHandlerRegistry
    ) -> None:
        self.container = container
        self.registry = registry

    async def create[E: DomainEvent](
        self, 
        event_type: type[E]
    ) -> list[DomainEventHandler[E]]:
        handler_types = self.registry.get(event_type)

        # async with self.container(scope=Scope.REQUEST) as container:
        return [
            await self.container.get(handler_type)
            for handler_type in handler_types
        ]
