from events.integration.event import IntegrationEvent
from events.integration.topology import Topic


def get_event_topic(event: IntegrationEvent) -> Topic:
    # Let's assume that at this project the format for integration events type
    # is {service}.{event_name}
    source = event.type.split(".")[0]
    return Topic(source)
