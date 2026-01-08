import json
from typing import Any, Iterable
# import logging

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from events.integration.bus import IntegrationEventBus
from events.integration.event import IntegrationEvent

from common.utils import get_event_topic

from user_service.infrastructure.outbox import Outbox
from user_service.infrastructure.outbox.outbox import OutboxItem
from user_service.infrastructure.persistence.models.outbox import OutboxEventModel


# logger = logging.getLogger(__name__)


class SQLOutboxItem(OutboxItem):
    def __init__(
        self,
        session: AsyncSession,
        model: OutboxEventModel, 
        event: IntegrationEvent
    ) -> None:
        super().__init__(event)

        self.model = model
        self.session = session

    async def mark_as_processed(self) -> None:
        await self.session.delete(self.model)


class SQLOutbox(Outbox):
    def __init__(
        self,
        session: AsyncSession
    ):
        self.session = session

    async def put(self, event: IntegrationEvent) -> None:
        data = event.to_dict()
        payload = json.dumps(data)

        self.session.add(OutboxEventModel(payload=payload))

    async def get_batch(self, batch_size: int = 500) -> Iterable[OutboxItem]:
        models = (await self.session.execute(
            select(OutboxEventModel)
                .with_for_update(skip_locked=True)
                .limit(batch_size)
        )).scalars().all()

        return [
            SQLOutboxItem(
                self.session,
                model,
                IntegrationEvent.from_dict(
                    json.loads(model.payload)
                )
            )
            for model in models
        ]
