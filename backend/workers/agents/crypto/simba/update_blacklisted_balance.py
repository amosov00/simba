import logging
from datetime import datetime, timedelta

from config import SIMBA_CONTRACT
from core.mechanics import SimbaWrapper
from database.crud import EthereumTransactionCRUD, MetaCRUD
from schemas import SimbaContractEvents, EthereumTransactionInDB, MetaSlugs, Meta
from workers.agents import app

__all__ = ["update_blacklisted_balance_job"]

update_blacklisted_balance_topic = app.topic(
    "update_blacklisted_balance", internal=True, retention=timedelta(minutes=10), partitions=1
)


@app.agent(update_blacklisted_balance_topic)
async def update_blacklisted_balance_job(stream):
    async for _ in stream:
        transactions = await EthereumTransactionCRUD.find(
            {
                "contract": SIMBA_CONTRACT.title,
                "event": SimbaContractEvents.BlacklistedAdded,
            }
        )
        total_balance = 0
        simba_instance = SimbaWrapper()

        for transaction in transactions:
            transaction = EthereumTransactionInDB(**transaction)

            address = transaction.args.get("account")
            tx_blacklist_removed = await EthereumTransactionCRUD.find_one(
                {
                    "event": SimbaContractEvents.BlacklistedRemoved,
                    "args.account": address,
                }
            )

            if not address or tx_blacklist_removed:
                continue

            total_balance += await simba_instance.balance_of(address)

        meta_instance = Meta(
            slug=MetaSlugs.BLACKLISTED_BALANCE, payload={"balance": total_balance}, updated_at=datetime.now()
        )
        await MetaCRUD.update_or_insert({"slug": MetaSlugs.BLACKLISTED_BALANCE}, meta_instance.dict())
        logging.info(f"Updated blacklisted balance: {total_balance}")

    return
