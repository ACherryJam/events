import abc

from events.integration.event import IntegrationEvent


class Consumer(abc.ABC):
    """An event bus consumer

    Override `on_event` method to handle integration events
    """
    def __init__(self, name: str) -> None:
        self.name = name
    
    @abc.abstractmethod
    async def on_event(self, event: IntegrationEvent) -> None:
        ...
