import json
import logging

from aio_pika import ExchangeType, Message
from aio_pika.abc import (
    AbstractRobustConnection, AbstractChannel, AbstractIncomingMessage, AbstractQueue
)

from events.integration.bus import IntegrationEventBus
from events.integration.event import IntegrationEvent
from events.integration.topology import IntegrationEventBusRegistration, Topic


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class RabbitMQIntegrationEventBus(IntegrationEventBus):
    def __init__(
        self, 
        connection: AbstractRobustConnection,
        registrations: list[IntegrationEventBusRegistration] | None = None
    ) -> None:
        super().__init__(registrations)

        self.connection = connection

        self.reading_channel: AbstractChannel | None = None
        self.writing_channel: AbstractChannel | None = None

        self._queues: list[AbstractQueue] = []
    
    async def startup(self) -> None:
        self.reading_channel = await self.connection.channel()
        self.writing_channel = await self.connection.channel()

        registrations = self.registrations.copy()
        for registration in registrations:
            await self._register_consumer(registration)
        
        logger.debug("Startup is complete")
    
    async def shutdown(self) -> None:
        for queue in self._queues:
            await queue.cancel(consumer_tag=str(id(queue)))

        if self.reading_channel is not None:
            await self.reading_channel.close()
        if self.writing_channel is not None:
            await self.writing_channel.close()
        
        logger.debug("Shutdown is complete")

    async def send(self, topic: Topic, event: IntegrationEvent) -> None:
        if self.writing_channel is None:
            raise RuntimeError("Channel is uninitialized. Make sure to run startup.")
        
        payload = event.to_dict()
        data = json.dumps(payload).encode("utf-8")

        exchange = await self.writing_channel.declare_exchange(
            name=topic.name,
            type=ExchangeType.DIRECT,
            durable=True
        )
        await exchange.publish(
            message=Message(data),
            routing_key=event.type
        )
    
    async def register(self, registration: IntegrationEventBusRegistration) -> None:
        await super().register(registration)

        if self.reading_channel is not None:
            await self._register_consumer(registration)

    async def _register_consumer(self, registration: IntegrationEventBusRegistration) -> None:
        if self.reading_channel is None:
            raise RuntimeError("Channel is uninitialized. Make sure to run startup.")

        queue = await self.reading_channel.declare_queue(
            registration.consumer.name,
            durable=True
        )
        exchange = await self.reading_channel.declare_exchange(
            registration.topic.name,
            type=ExchangeType.DIRECT,
            durable=True
        )

        for event in registration.events:
            await queue.bind(
                exchange, routing_key=event.type
            )
        
        async def on_message(message: AbstractIncomingMessage):
            data = message.body.decode("utf-8")
            payload = json.loads(data)
            event = IntegrationEvent.from_dict(payload)

            try:
                await registration.consumer.on_event(event)
                await message.ack()
            except Exception as e:
                logger.exception("Error occured when processing message", exc_info=e)
                await message.nack()

        self._queues.append(queue)
        await queue.consume(on_message, consumer_tag=str(id(queue)))
