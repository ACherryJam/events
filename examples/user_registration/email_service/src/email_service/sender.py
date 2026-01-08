import abc
import smtplib
import logging
from typing import Protocol


logger = logging.getLogger(__name__)


class EmailSender(Protocol):
    @abc.abstractmethod
    async def send_mail(self, sender: str, recipient: str, content: bytes) -> None:
        ...


class FakeSender(EmailSender):
    async def send_mail(self, sender: str, recipient: str, content: bytes) -> None:
        logger.info(
            f"Tried to send an email to {recipient} from {sender}."
        )


class SMTPSender(EmailSender):
    async def send_mail(self, sender: str, recipient: str, content: bytes) -> None:
        with smtplib.SMTP() as smtp:
            smtp.sendmail(
                sender,
                recipient,
                content
            )

