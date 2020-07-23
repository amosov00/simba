import smtplib
from http import HTTPStatus
from typing import Literal
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import urlencode

from fastapi import HTTPException
from sentry_sdk import capture_exception, capture_message
import httpx

from schemas import InvoiceInDB
from config import (
    EMAIL_LOGIN, EMAIL_PASSWORD, EMAIL_PORT, EMAIL_SERVER, HOST_URL, SIMBA_SUPPORT_EMAIL,
    MAILGUN_API_KEY, MAILGUN_DOMAIN_NAME, MAILGUN_MESSAGE_LINK,
)

__all__ = ["MailGunEmail"]


class Email:
    """Deprecated"""

    def __init__(self):
        self.email_from = EMAIL_LOGIN
        self.password = EMAIL_PASSWORD
        self.port = EMAIL_PORT
        self.server = EMAIL_SERVER
        self.mailserver = smtplib.SMTP_SSL(self.server, self.port)

    @staticmethod
    def _get_link(code: str, email: str, method: str) -> str:
        if method == "verification":
            params = {f"{method}_code": code, "email": email}
            return f"{HOST_URL}activate?{urlencode(params)}"
        if method == "recover":
            params = {f"{method}_code": code}
            return f"{HOST_URL}recover?{urlencode(params)}"

    def login(self) -> None:
        try:
            self.mailserver.login(self.email_from, self.password)
            return None
        except Exception as e:
            capture_exception(e)
            raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, "Error while sending email")

    def create_message(self, to: str, body: str) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg["From"] = self.email_from
        msg["Subject"] = "Simba"
        msg["To"] = to
        msg.attach(MIMEText(body, "html"))
        return msg

    def send_message(self, to: str, text: str):
        try:
            self.mailserver.sendmail(self.email_from, to, text)
            return None
        except Exception as e:
            capture_exception(e)
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Error while sending email")

    async def send_verification_code(self, to: str, code: str) -> None:
        self.login()
        msg = self.create_message(
            to,
            "Добрый день! <br>\n"
            'Перейдите по <a href="{}">этой</a> ссылке для регистрации в Simba<br>\n'
            "Надеемся вам понравится! До встречи!".format(Email._get_link(code, to, method="verification")),
        )
        self.send_message(to, msg.as_string())
        self.mailserver.quit()
        return None

    async def send_recover_code(self, to: str, code: str) -> None:
        self.login()
        msg = self.create_message(
            to,
            "Добрый день! <br>\n"
            'Перейдите по <a href="{}">этой</a> ссылке для восстановления пароля в Simba<br>\n'
            "До встречи!".format(Email._get_link(code, "", method="recover")),
        )
        self.send_message(to, msg.as_string())
        self.mailserver.quit()
        return None


class MailGunEmail:
    def __init__(self):
        self.api_key = MAILGUN_API_KEY
        self.domain = MAILGUN_DOMAIN_NAME
        self.send_message_link = MAILGUN_MESSAGE_LINK
        self.email_from = EMAIL_LOGIN

    @staticmethod
    def _get_link(code: str, email: str, method: str) -> str:
        if method == "verification":
            params = {f"{method}_code": code, "email": email}
            return f"{HOST_URL}activate?{urlencode(params)}"
        if method == "recover":
            params = {f"{method}_code": code}
            return f"{HOST_URL}recover?{urlencode(params)}"

    def _create_message(self, to: str, body: str, subject: str = "Simba verification message") -> dict:
        msg = {
            "from": f"Simba Stablecoin {self.email_from}",
            "subject": subject,
            "to": to,
            "html": body,
        }
        return msg

    async def _send_message(self, msg: dict) -> None:
        async with httpx.AsyncClient() as client:
            try:
                email_send = (
                    await client.post(
                        self.send_message_link,

                        auth=("api", self.api_key),
                        data=msg,
                    )
                )
            except Exception as e:
                capture_exception(e)
                raise HTTPException(HTTPStatus.BAD_REQUEST, f"Error while sending email, {e}")

        if email_send.json().get("message") != "Queued. Thank you.":
            capture_message(f"Error while sending email, response - {str(email_send.json())}", level="error")
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, f"Error while sending email, {str(email_send.json())}"
            )

        return None

    async def send_verification_code(self, to: str, code: str) -> None:

        msg = self._create_message(
            to,
            "Добрый день! <br>\n"
            'Перейдите по <a href="{}">этой</a> ссылке для регистрации в Simba<br>\n'
            "Надеемся вам понравится! До встречи!".format(MailGunEmail._get_link(code, to, method="verification")),
        )

        await self._send_message(msg)

        return None

    async def send_recover_code(self, to: str, code: str) -> None:
        msg = self._create_message(
            to,
            "Добрый день! <br>\n"
            'Перейдите по <a href="{}">этой</a> ссылке для восстановления пароля в Simba<br>\n'
            "До встречи!".format(MailGunEmail._get_link(code, "", method="recover")),
        )

        await self._send_message(msg)

        return None

    async def send_message_to_support(
            self,
            error_type: Literal["simba_issue", "simba_redeem", "sst_transfer", "btc"],
            **kwargs
    ) -> None:
        assert SIMBA_SUPPORT_EMAIL is not None
        assert error_type in ("simba_issue", "simba_redeem", "sst_transfer", "btc")

        if error_type == "simba_issue" or error_type == "sst_transfer":
            invoice: InvoiceInDB = kwargs["invoice"]
            customer_address: str = kwargs["customer_address"]
            amount: int = kwargs["amount"]
            body = f"<b>Error</b> while executing {' '.join(error_type.split('_'))}<br>" \
                   f"Invoice ID: {str(invoice.id) if invoice else '?'}<br>" \
                   f"Client address: {customer_address}<br>" \
                   f"Amount: {amount}<br>"
        elif error_type == "simba_redeem":
            invoice: InvoiceInDB = kwargs["invoice"]
            amount: int = kwargs["amount"]
            body = f"<b>Error</b> while executing {' '.join(error_type.split('_'))}<br>" \
                   f"Invoice ID: {str(invoice.id) if invoice else '?'}<br>" \
                   f"Amount: {amount}<br>"

        elif error_type == "btc":
            hot_wallet_balance = kwargs["hot_wallet_balance"]
            btc_amount_to_send = kwargs["btc_amount_to_send"]
            invoices_in_queue = kwargs["invoices_in_queue"]
            total_btc_amount_to_send = kwargs["total_btc_amount_to_send"]
            body = f"<b>Warning</b> while sending BTC from hot wallet<br>" \
                   f"Hot wallet balance: {hot_wallet_balance} Satoshi<br>" \
                   f"Satoshi amount to send {btc_amount_to_send}; " \
                   f"Total Satoshi amount to send {total_btc_amount_to_send}<br>" \
                   f"Invoices in queue: {invoices_in_queue}<br>"
        else:
            body = "Unknown error"

        msg = self._create_message(
            SIMBA_SUPPORT_EMAIL,
            body,
            subject="Warning/Error from Simba"
        )
        await self._send_message(msg)
        return None
