from datetime import timedelta

from core.mechanics.invoices import rescue_stucked_invoices
from workers.agents import app

__all__ = ["rescue_stucked_invoices_job"]

rescue_stucked_invoices_topic = app.topic(
    "rescue_stucked_invoices", internal=True, retention=timedelta(minutes=10), partitions=1
)


@app.agent(rescue_stucked_invoices_topic, concurrency=1)
async def rescue_stucked_invoices_job(stream):
    async for _ in stream:
        await rescue_stucked_invoices()

    return
