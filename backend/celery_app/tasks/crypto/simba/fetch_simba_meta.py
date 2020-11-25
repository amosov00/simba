import logging

from celery_app.celeryconfig import app
from core.integrations import EthplorerWrapper
from database.crud import MetaCRUD
from schemas import MetaSlugs

__all__ = ["fetch_simba_meta"]


@app.task(
    name="fetch_simba_meta",
    bind=True,
    retry_backoff=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5},
)
async def fetch_simba_meta(self, *args, **kwargs):
    payload = await EthplorerWrapper().fetch_simba_metadata()
    if payload:
        logging.info(f"Updated simba meta")
        await MetaCRUD.update_by_slug(MetaSlugs.SIMBA_META, payload)
    else:
        logging.error(f"Error updating simba meta")
    return True
