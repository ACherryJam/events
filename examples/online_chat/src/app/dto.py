from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field, TypeAdapter


class SocketMessage(BaseModel):
    """A message sent or received from a websocket"""
    type: str


class UserSocketMessage(SocketMessage):
    """A message received from a user
    
        :param request_id: 
            request id sent from the client. 
            Needed to correlate the message result response with the initial request.
        :type request_id: str
    """
    request_id: str


class SentChatMessageDTO(UserSocketMessage):
    """A chat message sent by the user"""
    type: Literal["message"] = "message"
    text: str


class ReceivedChatMessageDTO(SocketMessage):
    """A chat message received from the user"""
    type: Literal["message"] = "message"
    text: str


class SocketMessageResultDTO(SocketMessage):
    """Result response to a :ref:`UserSocketMessage`"""
    type: str = "result"
    result: str
    request_id: str


class SuccessfulResultDTO(UserSocketMessage):
    type: str = "result"
    result: Literal["ok"] = "ok"


class FailureResultDTO(UserSocketMessage):
    type: str = "result"
    result: Literal["fail"] = "fail"
    reason: str


class UserConnectedDTO(SocketMessage):
    type: Literal["user_connected"] = "user_connected"

    username: str


class UserDisconnectedDTO(SocketMessage):
    type: Literal["user_disconnected"] = "user_disconnected"

    username: str


UserMessages = Union[
    SentChatMessageDTO,
]

userMessageAdapter: TypeAdapter[UserMessages] = TypeAdapter(
    Annotated[
        UserMessages,
        Field(discriminator="type")
    ]
)
