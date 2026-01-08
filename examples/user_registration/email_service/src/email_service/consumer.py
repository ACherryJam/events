from events.integration.topology.consumer.handler import EventHandlerConsumer, EventHandlerRegistry

from common.contracts.user import UserRegisteredV1

from email_service.builder import build_email
from email_service.sender import EmailSender
from email_service.settings import EmailSettings


class EmailConsumer(EventHandlerConsumer):
    def __init__(
        self,
        sender: EmailSender,
        settings: EmailSettings
    ) -> None:
        handlers: EventHandlerRegistry = {
            UserRegisteredV1: [self.send_registration_email,]
        }
        super().__init__("email", handlers)

        self.sender = sender
        self.settings = settings
    
    async def send_registration_email(self, event: UserRegisteredV1) -> None:
        content = build_email(
            sender=self.settings.sender_address,
            recipient=event.email
        )
        await self.sender.send_mail(
            sender=self.settings.sender_address,
            recipient=event.email,
            content=content
        )
