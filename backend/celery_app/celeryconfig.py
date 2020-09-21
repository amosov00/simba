from celery import Celery
from celery.schedules import crontab

import celery_decorator_taskcls
import celery_pool_asyncio  # noqa

celery_pool_asyncio.__package__  # noqa

from config import *

__all__ = ["app"]

celery_decorator_taskcls.patch_celery()

CELERY_MONGO_DATABASE_URL = f"{MONGO_DATABASE_URL}{CELERY_DATABASE_NAME}"

# TODO deal with backend
app = Celery(main="celery_main", broker=CELERY_BROKER_URL, )  # backend=CELERY_MONGO_DATABASE_URL

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Moscow",
    enable_utc=True,
    imports=["celery_app.tasks", ],
)

app.conf.beat_schedule = {
    "finish_overdue_invoices": {
        "task": "finish_overdue_invoices",
        "schedule": crontab(minute="*/1"),
        "args": (),
    },
    "fetch_and_proceed_simba_contract": {
        "task": "fetch_and_proceed_simba_contract",
        "schedule": crontab(minute="*/1"),
        "args": (),
    },
    "send_btc_to_proceeding_invoices": {
        "task": "send_btc_to_proceeding_invoices",
        "schedule": crontab(minute="*/2"),
        "args": (),
    },
    "delete_unused_webhooks": {
        "task": "delete_unused_webhooks",
        "schedule": crontab(minute="20", hour="*/3"),
        "args": ()
    },
    "fetch_and_proceed_sst_contract": {
        "task": "fetch_and_proceed_sst_contract",
        "schedule": crontab(minute="30", hour="*/1"),
        "args": (),
    },
    "fetch_empty_btc_addresses_info": {
        "task": "fetch_empty_btc_addresses_info",
        "schedule": crontab(minute="0", hour="*/18"),
        "args": (),
    },
    "update_btc_addresses_info": {
        "task": "update_btc_addresses_info",
        "schedule": crontab(minute="0", hour="2", day_of_month="*/1"),
        "args": (),
    },
}
