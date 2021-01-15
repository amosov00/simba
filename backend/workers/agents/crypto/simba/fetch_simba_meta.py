import logging
from datetime import timedelta

from core.integrations import EthplorerWrapper
from database.crud import MetaCRUD
from schemas import MetaSlugs
from workers.agents import app

__all__ = ["fetch_simba_meta_job"]

fetch_simba_meta_topic = app.topic("fetch_simba_meta", internal=True, retention=timedelta(minutes=10), partitions=1)


@app.agent(fetch_simba_meta_topic, concurrency=1)
async def fetch_simba_meta_job(stream):
    async for _ in stream:
        payload = await EthplorerWrapper().fetch_simba_metadata()
        if payload:
            logging.info("Updated simba meta")
            await MetaCRUD.update_by_slug(MetaSlugs.SIMBA_META, payload, upsert=True)
        else:
            logging.info("Skipped updating meta")
    return True
