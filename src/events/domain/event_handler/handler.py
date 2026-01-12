import abc
from typing import ClassVar, Optional, Protocol, get_args, get_origin

from events.domain.event import DomainEvent


class DomainEventHandlerRegistry:
    def __init__(
        self, 
        handlers: Optional[dict[type[DomainEvent], list[type["DomainEventHandler"]]]] = None
    ) -> None:
        self.handlers = handlers or {}
    
    def add[E: DomainEvent](
        self,
        event: type[E],
        handler: type["DomainEventHandler[E]"]
    ) -> None:
        if event not in self.handlers:
            self.handlers[event] = []
        self.handlers[event].append(handler)
    
    def remove[E: DomainEvent](
        self,
        event: type[E],
        handler: type["DomainEventHandler[E]"]
    ) -> None:
        if event in self.handlers:
            self.handlers[event].remove(handler)
    
    def get[E: DomainEvent](self, event: type[E]) -> list[type["DomainEventHandler[E]"]]:
        return self.handlers.get(event, [])


class DomainEventHandler[E: DomainEvent](Protocol):
    registry: ClassVar[DomainEventHandlerRegistry] = DomainEventHandlerRegistry()

    def __init_subclass__(cls) -> None:
        for base in cls.__orig_bases__: # type: ignore
            if get_origin(base) is DomainEventHandler:
                event_type, *_ = get_args(base)
                DomainEventHandler.registry.add(event_type, cls)

    @abc.abstractmethod
    async def handle(self, event: E) -> None:
        ...
