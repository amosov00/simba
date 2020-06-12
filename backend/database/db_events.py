import logging
import sentry_sdk

from database.init import mongo_client
from database.crud import UserCRUD
from schemas import UserCreationNotSafe
from config import DEBUG, ENV

test_user = {
    "email": "admin@simba.com",
    "first_name": "admin",
    "last_name": "admin",
    "password": "a439a4dAA",
    "repeat_password": "a439a4dAA",
}

if DEBUG:
    test_user = {
        "email": "test@test.com",
        "first_name": "test",
        "last_name": "test",
        "password": "TestTest",
        "repeat_password": "TestTest",
    }


async def prepopulate_users():
    if not await UserCRUD.find_by_email(test_user["email"]):
        await UserCRUD.create_safe(
            user=UserCreationNotSafe(**test_user), is_active=True, is_superuser=True, email_is_active=True
        )

    return True


async def prepopulate_db():
    logging.info("Starting prepopulate db")
    is_failed = None

    try:
        await mongo_client.admin.command("ping")
    except Exception as e:
        is_failed = True
        logging.error(f"Unable to connect DB, error {e.__class__.__name__}")
        sentry_sdk.capture_exception(e)
        return None
    try:
        await prepopulate_users()
    except Exception as e:
        is_failed = True
        logging.error(f"Unable to create users, error {e.__class__.__name__}")
        sentry_sdk.capture_exception(e)

    if not is_failed:
        logging.info(f"Successfully prepopulated db")

    return True


async def close_db_connection():
    logging.info("Shutting down db connection")
    mongo_client.close()
