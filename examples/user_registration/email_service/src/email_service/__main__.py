import sys
import signal
import asyncio
import logging

from dishka import AsyncContainer, make_async_container
from events.integration.bus import IntegrationEventBus
from events.integration.topology import IntegrationEventBusRegistration

from common.rabbitmq import RabbitMQSettings, RabbitMQIntegrationEventBusProvider
from common.contracts.user.topic import UserServiceTopic
from common.log import ColoredFormatter

from email_service.consumer import EmailConsumer
from email_service.provider import EmailProvider
from email_service.settings import EmailSettings


logger = logging.getLogger("email_service")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

formatter = ColoredFormatter()
handler.setFormatter(formatter)

logger.addHandler(handler)


def create_container() -> AsyncContainer:
    return make_async_container(
        RabbitMQIntegrationEventBusProvider(),
        EmailProvider(),
        context={
            RabbitMQSettings: RabbitMQSettings(),  # type: ignore
            EmailSettings: EmailSettings()         # type: ignore
        }
    )


async def main():
    stopping = asyncio.Event()

    def handler(*_):
        stopping.set()
    
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    container = create_container()

    bus = await container.get(IntegrationEventBus)
    consumer = await container.get(EmailConsumer)

    await bus.register(
        IntegrationEventBusRegistration(
            consumer,
            UserServiceTopic,
            consumer.handlers.keys()
        )
    )
    await bus.startup()

    logger.info("Started the email service")
    await stopping.wait()
    logger.info("Stopping the email service...")

    await bus.shutdown()
    await container.close()


if __name__ == "__main__":
    asyncio.run(main())
