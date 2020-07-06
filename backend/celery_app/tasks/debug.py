from celery_app.celeryconfig import app

import logging

__all__ = ['debug_task_1']


@app.task(
    name="debug_task_1",
    bind=True,
    soft_time_limit=42,
    time_limit=300,
)
async def debug_task_1(self, *args, **kwargs):
    logging.info(f'Hello there debug_task_1')
    return True
