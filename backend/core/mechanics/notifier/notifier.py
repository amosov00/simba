import logging
from datetime import datetime, timedelta

from config import SUPPORT_FREQUENCY_LIMIT
from core.utils import Email
from database.crud import MetaCRUD
from schemas import MetaSlugs, Meta

__all__ = ["SupportNotifier"]


class NotifierHelper:
    @classmethod
    async def _is_allowed_to_send_to_support(cls, slug: str, frequency_limit: int = SUPPORT_FREQUENCY_LIMIT) -> bool:
        meta_email_time = await MetaCRUD.find_by_slug(slug, False) or {}
        if not meta_email_time:
            await cls._create_sent_at(slug)
        now = datetime.now()
        last_email_sent = meta_email_time.get("payload", {}).get("sent_at", now)
        return now - last_email_sent > timedelta(minutes=frequency_limit)

    @classmethod
    async def _update_sent_at(cls, slug):
        await MetaCRUD.update_by_slug(slug, {"sent_at": datetime.now()})
        return True

    @classmethod
    async def _create_sent_at(cls, slug):
        await MetaCRUD.insert_one(Meta(
            slug=slug,
            payload={"sent_at": datetime.now()}
        ).dict())
        return True


class SupportNotifier(NotifierHelper):
    async def hot_wallet_balance_lack(self, **kwargs) -> None:
        """
        Checks if email can be send and sends it
        :return:
        """
        if not await self._is_allowed_to_send_to_support(MetaSlugs.EMAIL_SUPPORT_HOT_WALLET_BALANCE_LACK):
            logging.info("Skipped message sending to support")
            return None

        await Email().support_hot_wallet_balance_lack(**kwargs)
        await self._update_sent_at(MetaSlugs.EMAIL_SUPPORT_HOT_WALLET_BALANCE_LACK)
        return

    async def invoice_stucked(self, **kwargs) -> None:
        """
        Checks if email can be send and sends it
        :return:
        """
        if not await self._is_allowed_to_send_to_support(MetaSlugs.EMAIL_SUPPORT_INVOICE_STUCK):
            logging.info("Skipped message sending to support")
            return

        await Email().support_invoice_stucked(**kwargs)
        await self._update_sent_at(MetaSlugs.EMAIL_SUPPORT_INVOICE_STUCK)
        return
