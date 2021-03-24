from http import HTTPStatus
from os.path import join
from typing import Literal
from urllib.parse import urlencode
from urllib.parse import urljoin

import httpx
from fastapi import HTTPException
from jinja2 import Environment, select_autoescape, FileSystemLoader
from sentry_sdk import capture_exception, capture_message
from tenacity import retry, stop_after_attempt, wait_fixed

from config import BASE_DIR, settings
from schemas import InvoiceInDB

__all__ = ["Email"]


class Email:
    def __init__(self):
        self.api_key = settings.email.mailgun_api_key
        self.domain = settings.email.mailgun_domain_name
        self.send_message_link = settings.email.mailgun_message_link
        self.email_from = settings.email.email_login
        self.support_mail = settings.common.support_email
        self.template_env = Environment(
            loader=FileSystemLoader(join(BASE_DIR, "templates")), autoescape=select_autoescape(["html"])
        )

    @staticmethod
    def _get_link(code: str, email: str, method: str) -> str:
        if method == "verification":
            params = {f"{method}_code": code, "email": email}
            return urljoin(settings.common.host_url, "activate?" + urlencode(params))
        if method == "recover":
            params = {f"{method}_code": code}
            return urljoin(settings.common.host_url, "recover?" + urlencode(params))

    def _render_template(self, template_filename: str, **kwargs):
        return self.template_env.get_template(f"{template_filename}.html").render(**kwargs)

    def create_message(self, to: str, subject: str, body: str) -> dict:
        return {"from": f"Simba Stablecoin {self.email_from}", "subject": subject, "to": to, "html": body, "text": body}

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
    async def _send_message(self, msg: dict) -> None:
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    self.send_message_link,
                    auth=("api", self.api_key),
                    data=msg,
                )
            except Exception as e:
                capture_exception(e)
                raise HTTPException(HTTPStatus.BAD_REQUEST, f"Error while sending email, {e}")

        if resp.json().get("message") != "Queued. Thank you.":
            capture_message(f"Error while sending email, response - {str(resp.json())}", level="error")

        return None

    async def send_verification_code(self, to: str, code: str) -> None:
        body = self._render_template("verification", to=to, link=self._get_link(code, to, method="verification"))
        msg = self.create_message(to=to, subject="Verification", body=body)
        await self._send_message(msg)
        return None

    async def send_recover_code(self, to: str, code: str) -> None:
        body = self._render_template("recover", to=to, link=self._get_link(code, "", method="recover"))
        msg = self.create_message(to=to, subject="Recover password", body=body)
        await self._send_message(msg)
        return None

    async def support_hot_wallet_balance_lack(self, **kwargs):
        msg = self.create_message(
            to=self.support_mail,
            subject="Warning: Hot wallet BTC balance lack",
            body=self._render_template("support-hot-wallet", **kwargs),
        )
        await self._send_message(msg)
        return None

    async def support_invoice_stucked(self, **kwargs):
        msg = self.create_message(
            to=self.support_mail,
            subject="Warning: Invoice Stucked",
            body=self._render_template("support-invoice-stuck", **kwargs),
        )
        await self._send_message(msg)
        return None

    async def new_suspended_invoice(self, **kwargs):
        msg = self.create_message(
            to=self.support_mail,
            subject="New suspended invoice",
            body=self._render_template("suspended-invoice", **kwargs),
        )
        await self._send_message(msg)
        return None

    async def send_message_to_support(
        self, error_type: Literal["simba_issue", "simba_redeem", "sst_transfer", "btc", "invoice_stucked"], **kwargs
    ) -> None:
        assert error_type in ("simba_issue", "simba_redeem", "sst_transfer", "btc", "invoice_stucked")

        subject = "Warning/Error from Simba"

        if error_type == "simba_issue" or error_type == "sst_transfer":
            invoice: InvoiceInDB = kwargs["invoice"]
            customer_address: str = kwargs["customer_address"]
            amount: int = kwargs["amount"]
            body = (
                f"<b>Error</b> while executing {' '.join(error_type.split('_'))}<br>"
                f"Invoice ID: {str(invoice.id) if invoice else '?'}<br>"
                f"Client address: {customer_address}<br>"
                f"Amount: {amount}<br>"
            )
        elif error_type == "simba_redeem":
            invoice: InvoiceInDB = kwargs["invoice"]
            amount: int = kwargs["amount"]
            body = (
                f"<b>Error</b> while executing {' '.join(error_type.split('_'))}<br>"
                f"Invoice ID: {str(invoice.id) if invoice else '?'}<br>"
                f"Amount: {amount}<br>"
            )

        else:
            body = "Unknown error"

        msg = self.create_message(settings.common.support_email, subject=subject, body=body)

        await self._send_message(msg)
        return None
