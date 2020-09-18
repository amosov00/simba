import logging
import sys
from datetime import datetime

import sentry_sdk

from config import ENV, BTC_COLD_WALLETS, BTC_COLD_XPUB_SWISS
from config import IS_PRODUCTION
from database.crud import UserCRUD, BTCxPubCRUD, MetaCRUD
from database.init import mongo
from schemas import UserCreationNotSafe, Meta, MetaSlugs, MetaManualPayoutPayload


async def test_db_connection():
    logging.info("Testing db connection")

    try:
        await mongo.client.admin.command("ping")
        logging.info("Successfully started db connection")
    except Exception as e:
        logging.error(f"Unable to connect DB, error {e.__class__.__name__}")
        sentry_sdk.capture_exception(e)
        return None


async def prepopulate_xpubs():
    if IS_PRODUCTION:
        if not await BTCxPubCRUD.find_by_title(BTC_COLD_XPUB_SWISS.title):
            await BTCxPubCRUD.insert_one(BTC_COLD_XPUB_SWISS.dict(exclude={"xpub"}))
    else:
        for wallet in BTC_COLD_WALLETS:
            if not await BTCxPubCRUD.find_by_title(wallet.title):
                await BTCxPubCRUD.insert_one(wallet.dict(exclude={"xpub"}))
    return True


async def prepopulate_meta():
    if not await MetaCRUD.find_by_slug(MetaSlugs.MANUAL_PAYOUT, raise_404=False):
        await MetaCRUD.insert_one(Meta(
            slug=MetaSlugs.MANUAL_PAYOUT,
            payload=MetaManualPayoutPayload(is_active=False).dict()
        ).dict())

    if not await MetaCRUD.find_by_slug(MetaSlugs.EMAIL_TO_SUPPORT_TIME, raise_404=False):
        await MetaCRUD.insert_one(Meta(
            slug=MetaSlugs.EMAIL_TO_SUPPORT_TIME,
            payload={"sent_at": datetime.now()}
        ).dict())
    return True


async def prepopulate_db():
    logging.info("Starting prepopulate db")

    try:
        await prepopulate_xpubs()
    except Exception as e:
        logging.error(f"Unable to create xpubs, error {e.__class__.__name__}")
        sentry_sdk.capture_exception(e)
        sys.exit(1)

    try:
        await prepopulate_meta()
    except Exception as e:
        logging.error(f"Unable to create meta, error {e.__class__.__name__}")
        sentry_sdk.capture_exception(e)
        sys.exit(1)

    logging.info(f"Successfully prepopulated db")
    return True


async def close_db_connection():
    logging.info("Shutting down db connection")
    mongo.close()
