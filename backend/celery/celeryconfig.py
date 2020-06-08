from celery import Celery, backends
from config import *

__all__ = ['celery_app']

celery_app = Celery(
    "celery",
    broker=CELERY_BROKER_URL,
)

celery_app.config_from_object('config', namespace='CELERY')

celery_app.conf.timezone = 'UTC'

celery_app.conf.beat_schedule = {
    'DEBUG': {
        'task': 'core.tasks.celery.debug_task',
        'schedule': 5,
        'args': ()
    },
}



