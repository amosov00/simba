from celery import Celery
import celery_decorator_taskcls
import celery_pool_asyncio # noqa
celery_pool_asyncio.__package__ # noqa

from config import *

__all__ = ['celery_instance']

celery_decorator_taskcls.patch_celery()

CELERY_MONGO_DATABASE_URL = f"{MONGO_DATABASE_URL}{CELERY_DATABASE_NAME}"

celery_instance = Celery(
    main="celery_main",
    broker=CELERY_BROKER_URL,
    backend=CELERY_MONGO_DATABASE_URL,
)

celery_instance.conf.timezone = 'UTC'

celery_instance.conf.beat_schedule = {
}



