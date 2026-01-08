import dataclasses
from typing import ClassVar


@dataclasses.dataclass(unsafe_hash=True)
class EventKey:
    event_name: str
    version: int


class EventRegistry:
    def __init__(self) -> None:
        self.events: dict[EventKey, type[IntegrationEvent]] = {}

    def add(self, key: EventKey, event_type: type[IntegrationEvent]):
        if key in self.events:
            raise ValueError(f"Tried to add event type {event_type} when "
                             f"event {self.events[key]} is already registered under the key {key}")
        self.events[key] = event_type

    def get(self, key: EventKey) -> type[IntegrationEvent]:
        return self.events[key]


@dataclasses.dataclass
class IntegrationEvent:
    type: ClassVar[str]
    version: ClassVar[int]

    registry: ClassVar[EventRegistry] = EventRegistry()

    def __init_subclass__(cls, **_) -> None:
        if not hasattr(cls, "type") or not hasattr(cls, "version"):
            raise ValueError("A subclass must set values of \"type\" and \"version\" properties")
        
        IntegrationEvent.registry.add(
            EventKey(cls.type, cls.version), cls
        )

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "version": self.version,
            **dataclasses.asdict(self)
        }

    @staticmethod
    def from_dict(payload: dict) -> "IntegrationEvent":
        _type = payload.pop("type")
        version = payload.pop("version")

        event_type = IntegrationEvent.registry.get(EventKey(_type, version))
        return event_type(**payload)
