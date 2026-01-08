from events.domain.event import DomainEvent


class DomainEntity:
    def __init__(self) -> None:
        self.events: list[DomainEvent] = []
    
    def store_event(self, event: DomainEvent) -> None:
        self.events.append(event)
    
    def pop_events(self) -> list[DomainEvent]:
        events = self.events.copy()
        self.events.clear()

        return events
    