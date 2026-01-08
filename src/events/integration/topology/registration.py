from typing import Iterable
from dataclasses import dataclass

from events.integration.event import IntegrationEvent
from events.integration.topology.topic import Topic
from events.integration.topology.consumer.base import Consumer


@dataclass
class IntegrationEventBusRegistration:
    """Registers a `consumer` that listens for `events` in a specified `topic`"""
    consumer: Consumer
    topic: Topic
    events: Iterable[type[IntegrationEvent]]
