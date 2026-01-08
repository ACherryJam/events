import pathlib
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from events.integration.bus import IntegrationEventBus
from events.integration.topology import Topic, IntegrationEventBusRegistration
from events.integration.topology.consumer import EventHandlerConsumer

from app.user import User
from app.message import Message
from app.bus import RedisIntegrationEventBus
from app.events import MessageSent, UserConnected, UserDisconnected
from app.dto import FailureResultDTO, SentChatMessageDTO, SuccessfulResultDTO, userMessageAdapter


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.bus = RedisIntegrationEventBus("redis://localhost")
    await app.state.bus.startup()

    yield

    await app.state.bus.shutdown()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def index():
    return FileResponse(
        path=pathlib.Path(".").absolute() / "static" / "index.html"
    )


@app.websocket("/chat")
async def chat(
    socket: WebSocket
):
    user = User(socket)

    room_id = socket.query_params["room_id"]
    username = socket.query_params["username"]

    bus: IntegrationEventBus = app.state.bus

    async def message_handler(event: MessageSent):
        await user.send_message(
            message=Message(
                event.username, event.message
            )
        )
    
    async def user_connected_handler(event: UserConnected):
        await user.notify_of_user_connection(
            username=event.username
        )
    
    async def user_disconnected_handler(event: UserDisconnected):
        await user.notify_of_user_disconnection(
            username=event.username
        )

    consumer = EventHandlerConsumer(
        name=username, 
        handlers={
            MessageSent: [message_handler],
            UserConnected: [user_connected_handler],
            UserDisconnected: [user_disconnected_handler]
        }
    )

    registration = IntegrationEventBusRegistration(
        consumer,
        Topic(room_id),
        [MessageSent, UserConnected, UserDisconnected]
    )
    await bus.register(registration)

    try:
        await socket.accept()
        print('accepted')

        await bus.send(Topic(room_id), UserConnected(room_id, username))

        while True:
            text = await socket.receive_text()
            dto = userMessageAdapter.validate_json(text)

            try:
                match dto:
                    case SentChatMessageDTO():
                        await bus.send(
                            Topic(name=room_id),
                            MessageSent(
                                username=username,
                                message=dto.text
                            )
                        )
                    case _:
                        raise Exception("Unknown message")
            except:
                failure_result = FailureResultDTO(
                    request_id=dto.request_id,
                    reason="idk"
                )
                await socket.send_text(failure_result.model_dump_json())
            else:
                successful_result = SuccessfulResultDTO(request_id=dto.request_id)
                await socket.send_text(successful_result.model_dump_json())
    except WebSocketDisconnect:
        print("Websocket disconnected")
    except Exception as e:
        print("Error occured", e)
    finally:
        await bus.send(Topic(room_id), UserDisconnected(room_id, username))
        await bus.unregister(registration)
