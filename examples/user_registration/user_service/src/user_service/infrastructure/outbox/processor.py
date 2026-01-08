import asyncio
import datetime
import logging

from dishka import AsyncContainer, Scope
from events.integration.bus import IntegrationEventBus

from common.utils import get_event_topic
from user_service.application.transaction import Transaction

from .outbox import Outbox


logger = logging.getLogger(__name__)


class OutboxProcessor:
    def __init__(self, container: AsyncContainer) -> None:
        self.container = container

        self.bus: IntegrationEventBus | None = None
        self.task: asyncio.Task | None = None
        
    
    async def startup(self) -> None:
        self.bus = await self.container.get(IntegrationEventBus)
        
        if self.task is not None:
            self.task.cancel()

        self.task = asyncio.create_task(
            self._process_task()
        )
    
    async def shutdown(self) -> None:
        if self.task is not None:
            self.task.cancel()
            self.task = None
    
    async def process(self) -> None:
        if self.bus is None:
            raise Exception("Integration bus is not initialized. Make sure to run startup.")
        
        async with self.container(scope=Scope.REQUEST) as container:
            outbox = await container.get(Outbox)
            transaction = await container.get(Transaction)

            try:
                items = await outbox.get_batch(750)

                for item in items:
                    await self.bus.send(
                        topic=get_event_topic(item.event),
                        event=item.event
                    )
                    await item.mark_as_processed()

                await transaction.commit()
                logger.debug(f"Processed outbox at {datetime.datetime.now()}")
            except Exception as e:
                await transaction.rollback()
                logger.exception(
                    f"Failed to process outbox at {datetime.datetime.now()}",
                    exc_info=e
                )

    async def _process_task(self) -> None:
        # TODO: handle cancellation
        while True:
            await self.process()
            await asyncio.sleep(1.0)
