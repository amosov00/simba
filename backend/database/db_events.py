import logging
import sys

import sentry_sdk

from config import ENV, IS_PRODUCTION, BTC_COLD_WALLETS
from database.crud import UserCRUD, BTCxPubCRUD
from database.init import mongo_client
from schemas import UserCreationNotSafe

if IS_PRODUCTION:
    admin_user = {
        "email": "admin@simba.storage",
        "first_name": "admin",
        "last_name": "admin",
        "password": "77F2QQjcItQI",
        "repeat_password": "77F2QQjcItQI",
    }
elif ENV == "develop":
    admin_user = {
        "email": "admin@simba.com",
        "first_name": "admin",
        "last_name": "admin",
        "password": "a439a4dAA",
        "repeat_password": "a439a4dAA",
    }
else:
    admin_user = {
        "email": "test@test.com",
        "first_name": "test",
        "last_name": "test",
        "password": "TestTest",
        "repeat_password": "TestTest",
    }


async def prepopulate_users():
    if not await UserCRUD.find_by_email(admin_user["email"]):
        await UserCRUD.create_not_safe(
            user=UserCreationNotSafe(**admin_user), is_active=True, is_superuser=True, email_is_active=True,
        )

    return True


async def prepopulate_xpubs():
    for wallet in BTC_COLD_WALLETS:
        if not await BTCxPubCRUD.find_by_title(wallet.title):
            await BTCxPubCRUD.insert_one(
                wallet.dict()
            )
    return True


async def prepopulate_db():
    logging.info("Starting prepopulate db")

    try:
        await mongo_client.admin.command("ping")
    except Exception as e:
        logging.error(f"Unable to connect DB, error {e.__class__.__name__}")
        sentry_sdk.capture_exception(e)
        sys.exit(1)

    try:
        await prepopulate_users()
    except Exception as e:
        logging.error(f"Unable to create users, error {e.__class__.__name__}")
        sentry_sdk.capture_exception(e)
        sys.exit(1)

    try:
        await prepopulate_xpubs()
    except Exception as e:
        logging.error(f"Unable to create users, error {e.__class__.__name__}")
        sentry_sdk.capture_exception(e)
        sys.exit(1)

    logging.info(f"Successfully prepopulated db")
    return True


async def close_db_connection():
    logging.info("Shutting down db connection")
    mongo_client.close()
