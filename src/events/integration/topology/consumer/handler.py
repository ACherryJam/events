import asyncio
import warnings
from typing import Any, Callable, Coroutine, Optional

from events.integration.event import IntegrationEvent

from .base import Consumer


type EventHandler[E: IntegrationEvent] = Callable[[E], Coroutine[Any, Any, None]]
type EventHandlerRegistry = dict[type[IntegrationEvent], list[EventHandler]]


class EventHandlerConsumer(Consumer):
    def __init__(
        self, 
        name: str, 
        handlers: Optional[EventHandlerRegistry] = None
    ) -> None:
        super().__init__(name)

        self.handlers: EventHandlerRegistry = handlers or {}

    def add_handler[E: IntegrationEvent](
        self, event_type: type[E], handler: EventHandler[E]
    ) -> None:
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    async def on_event(self, event: IntegrationEvent) -> None:
        event_type = event.__class__
        if event_type not in self.handlers:
            warnings.warn(f"Received event {event} that doesn't have a handler for it")
        
        tasks = [
            asyncio.create_task(handler(event))
            for handler in self.handlers[event_type]
        ]
        await asyncio.gather(*tasks)
