import logging
from abc import ABC, abstractmethod
from email.message import EmailMessage

import aiosmtplib

from app.core.config import settings

logger = logging.getLogger(__name__)


def get_email_service() -> EmailService:
    match settings.EMAIL_BACKEND:
        case "smtp":
            return SmtpEmailService()
        case "console":
            return ConsoleEmailService()
        case "disabled":
            return DisabledEmailService()
        case _:
            raise RuntimeError(f"Unknown EMAIL_BACKEND: {settings.EMAIL_BACKEND}")


class EmailService(ABC):
    @abstractmethod
    async def send(
        self,
        to: str,
        subject: str,
        text: str,
        html: str | None = None,
    ) -> None: ...


class SmtpEmailService(EmailService):
    async def send(
        self,
        to: str,
        subject: str,
        text: str,
        html: str | None = None,
    ) -> None:
        message = EmailMessage()
        message["From"] = settings.EMAIL_FROM
        message["To"] = to
        message["Subject"] = subject

        if html:
            message.set_content(text)
            message.add_alternative(html, subtype="html")
        else:
            message.set_content(text)

        kwargs = dict(
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            start_tls=settings.SMTP_USE_TLS,
            use_tls=settings.SMTP_USE_SSL,
            timeout=10,
        )

        # guard against including empty username/password
        if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
            kwargs["username"] = settings.SMTP_USERNAME
            kwargs["password"] = settings.SMTP_PASSWORD

        await aiosmtplib.send(message, **kwargs)  # type: ignore


class ConsoleEmailService(EmailService):
    async def send(
        self,
        to: str,
        subject: str,
        text: str,
        html: str | None = None,
    ) -> None:
        logger.info(
            "EMAIL (console)\nTo: %s\nSubject: %s\n\n%s",
            to,
            subject,
            text,
        )


class DisabledEmailService(EmailService):
    async def send(
        self,
        to: str,
        subject: str,
        text: str,
        html: str | None = None,
    ) -> None:
        logger.debug("Email disabled; skipping send to %s", to)
