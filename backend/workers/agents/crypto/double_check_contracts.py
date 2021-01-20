import logging

from config import SIMBA_CONTRACT, SST_CONTRACT
from core.integrations.ethereum import EventsContractWrapper
from workers.agents import app

__all__ = ["double_check_contracts_job"]

double_check_contracts_topic = app.topic("double_check_contracts", internal=True, partitions=1)


@app.agent(double_check_contracts_topic, concurrency=1)
async def double_check_contracts_job(stream):
    """Синхронизация с Simba, SST контрактом."""
    async for _ in stream:
        for i in (SIMBA_CONTRACT, SST_CONTRACT):
            await EventsContractWrapper(i).fetch_missing_blocks()
        logging.info("Checked for missed transactions")

    return True
