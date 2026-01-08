from dataclasses import dataclass

from events.integration.event import IntegrationEvent


@dataclass
class MessageSent(IntegrationEvent):
    type = "chat.message_sent"
    version = 1

    username: str
    message: str


@dataclass 
class UserConnected(IntegrationEvent):
    type = "chat.user_connected"
    version = 1

    room_id: str
    username: str


@dataclass 
class UserDisconnected(IntegrationEvent):
    type = "chat.user_disconnected"
    version = 1

    room_id: str
    username: str
