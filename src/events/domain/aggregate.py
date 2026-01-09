from .event import DomainEvent


class AggregateRoot:
    def __init__(self) -> None:
        self.events: list[DomainEvent] = []
    
    def publish_event(self, event: DomainEvent) -> None:
        self.events.append(event)
    
    def pop_events(self) -> list[DomainEvent]:
        events = self.events.copy()
        self.events.clear()

        return events
