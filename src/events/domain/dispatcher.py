import asyncio
from typing import Iterable

from events.domain.event import DomainEvent
from events.domain.aggregate import AggregateRoot
from events.domain.event_handler.factory import DomainEventHandlerFactory


class DomainEventDispatcher:
    def __init__(
        self,
        handler_factory: DomainEventHandlerFactory
    ) -> None:
        self.handler_factory = handler_factory

        self.events: list[DomainEvent] = []

    def store_event(self, event: DomainEvent) -> None:
        self.events.append(event)

    def store_events(self, events: Iterable[DomainEvent]) -> None:
        self.events.extend(events)
    
    def from_entity(self, entity: AggregateRoot) -> None:
        self.store_events(entity.pop_events())
    
    async def process(self) -> None:
        events = self.events.copy()
        self.events.clear()

        for event in events:
            await self._process_event(event)
    
    async def _process_event(self, event: DomainEvent) -> None:
        handlers = await self.handler_factory.create(event.__class__)

        coros = [
            handler.handle(event)
            for handler in handlers
        ]
        await asyncio.gather(*coros)

    async def __aenter__(self) -> None:
        pass

    async def __aexit__(self, exc_type, exc, tb):
        if exc is None:
            await self.process()
    