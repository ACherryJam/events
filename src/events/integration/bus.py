import abc
from typing import Optional

from events.integration.event import IntegrationEvent
from events.integration.topology import Topic, IntegrationEventBusRegistration


class IntegrationEventBus(abc.ABC):
    def __init__(
        self, registrations: Optional[list[IntegrationEventBusRegistration]] = None
    ) -> None:
        self.registrations = registrations or []
    
    async def register(self, registration: IntegrationEventBusRegistration) -> None:
        self.registrations.append(registration)
    
    async def unregister(self, registration: IntegrationEventBusRegistration) -> None:
        self.registrations.remove(registration)

    @abc.abstractmethod
    async def send(self, topic: Topic, event: IntegrationEvent) -> None:
        ...

    async def startup(self) -> None:
        ...

    async def shutdown(self) -> None:
        ...
