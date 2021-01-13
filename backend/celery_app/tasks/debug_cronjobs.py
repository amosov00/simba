import logging

from celery_app.celeryconfig import app

__all__ = ["debug_cronjob_1"]


@app.task(
    name="debug_cronjob_1",
    bind=True,
    retry_backoff=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5},
)
async def debug_cronjob_1(self, *args, **kwargs):
    logging.info("Hello there debug_cronjob_1")
    return True
