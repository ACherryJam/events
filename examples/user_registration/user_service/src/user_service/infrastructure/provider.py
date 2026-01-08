from typing import Iterable

from dishka import Provider

from common.rabbitmq.provider import RabbitMQIntegrationEventBusProvider

from user_service.infrastructure.persistence.provider import SQLAlchemyPersistenceProvider
from user_service.infrastructure.event_handlers.provider import InfrastructureDomainEventHandlersProvider


def get_infrastructure_providers() -> Iterable[Provider]:
    return [
        SQLAlchemyPersistenceProvider(),
        RabbitMQIntegrationEventBusProvider(),
        InfrastructureDomainEventHandlersProvider()
    ]
