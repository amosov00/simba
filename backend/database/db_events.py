import logging
import sys
from datetime import datetime

import sentry_sdk

from config import BTC_COLD_WALLETS
from database.crud import BTCxPubCRUD, MetaCRUD
from database.init import mongo
from schemas import Meta, MetaSlugs, MetaManualPayoutPayload


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
    for wallet in BTC_COLD_WALLETS:
        if not wallet.xpub:
            continue
        if not await BTCxPubCRUD.find_by_title(wallet.title):
            await BTCxPubCRUD.insert_one(wallet.dict(exclude={"xpub"}))
    return True


async def prepopulate_meta():
    if not await MetaCRUD.find_by_slug(MetaSlugs.MANUAL_PAYOUT, raise_404=False):
        await MetaCRUD.insert_one(Meta(
            slug=MetaSlugs.MANUAL_PAYOUT,
            payload=MetaManualPayoutPayload(is_active=False).dict()
        ).dict())

    if not await MetaCRUD.find_by_slug(MetaSlugs.EMAIL_SUPPORT_HOT_WALLET_BALANCE_LACK, raise_404=False):
        await MetaCRUD.insert_one(Meta(
            slug=MetaSlugs.EMAIL_TO_SUPPORT_TIME,
            payload={"sent_at": datetime.now()}
        ).dict())

    if not await MetaCRUD.find_by_slug(MetaSlugs.EMAIL_SUPPORT_INVOICE_STUCK, raise_404=False):
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
