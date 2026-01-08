import json
from fastapi import WebSocket

from app.dto import ReceivedChatMessageDTO, UserConnectedDTO, UserDisconnectedDTO
from app.message import Message


class User:
    def __init__(
        self, 
        socket: WebSocket
    ) -> None:
        self.socket = socket
    
    async def send_message(self, message: Message):
        dto = ReceivedChatMessageDTO(
            text=f"{message.username}: {message.message}"
        )
        await self.socket.send_json(dto.model_dump())
    
    async def notify_of_user_connection(self, username: str):
        dto = UserConnectedDTO(username=username)
        await self.socket.send_json(dto.model_dump())

    async def notify_of_user_disconnection(self, username: str):
        dto = UserDisconnectedDTO(username=username)
        await self.socket.send_json(dto.model_dump())