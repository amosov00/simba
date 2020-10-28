import logging

from celery_app.celeryconfig import app
from core.integrations.ethereum import EventsContractWrapper
from config import SIMBA_CONTRACT, SST_CONTRACT

__all__ = ["double_check_contracts"]


@app.task(
    name="double_check_contracts",
    bind=True,
    retry_backoff=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5},
)
async def double_check_contracts():
    """Синхронизация с Simba контрактом"""
    for i in (SIMBA_CONTRACT, SST_CONTRACT):
        await EventsContractWrapper(i).fetch_missing_blocks()
    logging.info(f"Checked for missed transactions")
    return True
