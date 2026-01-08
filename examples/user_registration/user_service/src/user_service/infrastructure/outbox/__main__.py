import logging
import signal
import asyncio

from dishka import AsyncContainer, make_async_container
from events.integration.bus import IntegrationEventBus

from common.rabbitmq.settings import RabbitMQSettings
from common.log import configure_logger

from user_service.application.provider import get_application_providers
from user_service.infrastructure.outbox.processor import OutboxProcessor
from user_service.infrastructure.persistence.settings import SQLPersistenceSettings
from user_service.infrastructure.provider import get_infrastructure_providers


logger = logging.getLogger(__package__)
logger.setLevel(logging.DEBUG)

configure_logger(logger)


def create_container() -> AsyncContainer:
    return make_async_container(
        *get_application_providers(),
        *get_infrastructure_providers(),
        context={
            SQLPersistenceSettings: SQLPersistenceSettings(),
            RabbitMQSettings: RabbitMQSettings(),
        }
    )


async def main():
    stopping = asyncio.Event()

    def handler(*_):
        stopping.set()
    
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    container = create_container()
    
    processor = OutboxProcessor(container)
    bus = await container.get(IntegrationEventBus)

    await bus.startup()
    await processor.startup()
    logger.info("Started outbox process")

    await stopping.wait()

    await processor.shutdown()
    await bus.shutdown()
    logger.info("Stopped outbox process")

    await container.close()


if __name__ == "__main__":
    asyncio.run(main())
