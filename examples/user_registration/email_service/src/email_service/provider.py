

from dishka import Provider, Scope, from_context, provide

from email_service.consumer import EmailConsumer
from email_service.sender import EmailSender, FakeSender
from email_service.settings import EmailSettings


class EmailProvider(Provider):
    settings = from_context(
        EmailSettings,
        scope=Scope.APP
    )

    sender = provide(
        provides=EmailSender,
        source=FakeSender,
        scope=Scope.APP
    )

    consumer = provide(
        EmailConsumer,
        scope=Scope.APP
    )
    