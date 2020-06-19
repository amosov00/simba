from core.integrations.ethereum import ContractEventsWrapper
from celery_app.celeryconfig import app
from config import SIMBA_CONTRACT

__all__ = ['fetch_simba_contract_cronjob']


@app.task(
    name="fetch_simba_contract",
    bind=True,
    soft_time_limit=42,
    time_limit=300,
)
async def fetch_simba_contract_cronjob(self, *args, **kwargs):
    await ContractEventsWrapper(SIMBA_CONTRACT).fetch_blocks_and_save()
    return True
