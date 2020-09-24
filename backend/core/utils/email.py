from os.path import join
from http import HTTPStatus
from typing import Literal
from urllib.parse import urlencode

import httpx
from fastapi import HTTPException
from sentry_sdk import capture_exception, capture_message
from tenacity import retry, stop_after_attempt, wait_fixed
from jinja2 import Environment, select_autoescape, FileSystemLoader

from schemas import InvoiceInDB
from config import (
    BASE_DIR, EMAIL_LOGIN, HOST_URL, SIMBA_SUPPORT_EMAIL,
    MAILGUN_API_KEY, MAILGUN_DOMAIN_NAME, MAILGUN_MESSAGE_LINK,
)

__all__ = ["Email"]


class Email:
    def __init__(self):
        self.api_key = MAILGUN_API_KEY
        self.domain = MAILGUN_DOMAIN_NAME
        self.send_message_link = MAILGUN_MESSAGE_LINK
        self.email_from = EMAIL_LOGIN
        self.template_env = Environment(
            loader=FileSystemLoader(join(BASE_DIR, "templates")),
            autoescape=select_autoescape(['html'])
        )

    @staticmethod
    def _get_link(code: str, email: str, method: str) -> str:
        if method == "verification":
            params = {f"{method}_code": code, "email": email}
            return f"{HOST_URL}activate?{urlencode(params)}"
        if method == "recover":
            params = {f"{method}_code": code}
            return f"{HOST_URL}recover?{urlencode(params)}"

    def _render_template(self, template_filename: str, **kwargs):
        return self.template_env.get_template(f"{template_filename}.html").render(**kwargs)

    def _create_message(self, to: str, subject: str, body: str) -> dict:
        msg = {
            "from": f"Simba Stablecoin {self.email_from}",
            "subject": subject,
            "to": to,
            "html": body,
            "text": body
        }
        return msg

    # @classmethod
    # async def _is_allowed_to_send_to_support(cls, frequency_limit: int = 10) -> bool:
    #     meta_email_time = await MetaCRUD.find_by_slug(MetaSlugs.EMAIL_TO_SUPPORT_TIME) or {}
    #     now = datetime.now()
    #     last_email_sent = meta_email_time.get("args", {}).get("sent_at", now)
    #     return now - last_email_sent > timedelta(minutes=frequency_limit)
    #
    # @classmethod
    # async def _update_email_to_support_time_meta(cls):
    #     await MetaCRUD.update_by_slug(MetaSlugs.EMAIL_TO_SUPPORT_TIME, {"sent_at": datetime.now()})
    #     return True

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
    async def _send_message(self, msg: dict) -> None:
        async with httpx.AsyncClient() as client:
            try:
                resp = (
                    await client.post(
                        self.send_message_link,
                        auth=("api", self.api_key),
                        data=msg,
                    )
                )
            except Exception as e:
                capture_exception(e)
                raise HTTPException(HTTPStatus.BAD_REQUEST, f"Error while sending email, {e}")

        if resp.json().get("message") != "Queued. Thank you.":
            capture_message(f"Error while sending email, response - {str(resp.json())}", level="error")

        return None

        # if resp.text and resp.json().get("message") != "Queued. Thank you.":
        #     return None
        # else:
        #     capture_message(f"Error while sending email, response - {str(resp.json())}", level="error")
        #     raise HTTPException(
        #         HTTPStatus.BAD_REQUEST, f"Error while sending email, {str(resp.json())}"
        #     )

    async def send_verification_code(self, to: str, code: str) -> None:

        msg = self._create_message(
            to,
            subject="Simba verification",
            body="Добрый день! <br>\n"
                 'Перейдите по <a href="{}">этой</a> ссылке для регистрации в Simba<br>\n'
                 "Надеемся вам понравится! До встречи!".format(Email._get_link(code, to, method="verification")),
        )

        await self._send_message(msg)

        return None

    async def send_recover_code(self, to: str, code: str) -> None:
        msg = self._create_message(
            to,
            subject="Восстановления пароля",
            body="Добрый день! <br>\n"
                 'Перейдите по <a href="{}">этой</a> ссылке для восстановления пароля в Simba<br>\n'
                 "До встречи!".format(Email._get_link(code, "", method="recover")),
        )

        await self._send_message(msg)

        return None

    async def send_message_to_support(
            self,
            error_type: Literal["simba_issue", "simba_redeem", "sst_transfer", "btc", "invoice_stucked"],
            **kwargs
    ) -> None:
        assert SIMBA_SUPPORT_EMAIL is not None
        assert error_type in ("simba_issue", "simba_redeem", "sst_transfer", "btc", "invoice_stucked")

        subject = "Warning/Error from Simba"

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

        elif error_type == "invoice_stucked":
            invoice: InvoiceInDB = kwargs["invoice"]
            body = f"<b>Warning:</b> invoice <br>" \
                   f"Invoice ID: {str(invoice.id)}<br>" \
                   f"Invoice Type: {invoice.invoice_type}<br>" \
                   f"Invoice Status: {invoice.status}<br>" \
                   f"Simba to sent: {invoice.simba_amount_proceeded} Satoshi<br>" \
                   f"Invoice created at: {invoice.created_at}"

        else:
            body = "Unknown error"

        msg = self._create_message(
            SIMBA_SUPPORT_EMAIL,
            subject=subject,
            body=body,
        )

        await self._send_message(msg)
        # circular import error
        # if limit_sending and await self._is_allowed_to_send_to_support(10):
        #     await self._send_message(msg)
        #     await self._update_email_to_support_time_meta()
        #
        # elif not limit_sending:
        #     await self._send_message(msg)
        #     await self._update_email_to_support_time_meta()

        return None
