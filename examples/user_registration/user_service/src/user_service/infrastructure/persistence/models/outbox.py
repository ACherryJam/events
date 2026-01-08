from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class OutboxEventModel(BaseModel):
    __tablename__ = "outbox_events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    payload: Mapped[str]
