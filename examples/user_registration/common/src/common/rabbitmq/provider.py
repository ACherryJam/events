from typing import AsyncIterable

from dishka import Provider, Scope, from_context, provide
from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustConnection
from events.integration.bus import IntegrationEventBus

from .bus import RabbitMQIntegrationEventBus
from .settings import RabbitMQSettings


class RabbitMQIntegrationEventBusProvider(Provider):
    settings = from_context(
        RabbitMQSettings,
        scope=Scope.APP
    )

    @provide(scope=Scope.APP)
    async def provide_bus(self, connection: AbstractRobustConnection) -> IntegrationEventBus:
        return RabbitMQIntegrationEventBus(
            connection=connection
        )

    @provide(scope=Scope.APP)
    async def provide_connection(
        self, settings: RabbitMQSettings
    ) -> AsyncIterable[AbstractRobustConnection]:
        conn = await connect_robust(
            url=settings.url
        )

        yield conn
        
        await conn.close()
