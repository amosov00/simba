import logging
from datetime import datetime

from celery_app.celeryconfig import app
from database.crud import EthereumTransactionCRUD, MetaCRUD
from schemas import SimbaContractEvents, EthereumTransactionInDB, MetaSlugs, Meta
from core.mechanics import SimbaWrapper
from config import SIMBA_CONTRACT

__all__ = ["update_blacklisted_balance"]


@app.task(
    name="update_blacklisted_balance",
    bind=True,
    retry_backoff=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5},
)
async def update_blacklisted_balance(self, *args, **kwargs):
    transactions = await EthereumTransactionCRUD.find({
        "contract": SIMBA_CONTRACT.title,
        "event": SimbaContractEvents.BlacklistedAdded,
    })
    total_balance = 0
    simba_instance = SimbaWrapper()

    for transaction in transactions:
        transaction = EthereumTransactionInDB(**transaction)

        address = transaction.args.get("account")
        tx_blacklist_removed = await EthereumTransactionCRUD.find_one({
            "event": SimbaContractEvents.BlacklistedRemoved,
            "args.account": address,
        })

        if not address or tx_blacklist_removed:
            continue

        total_balance += simba_instance.balance_of(address)

    meta_instance = Meta(
        slug=MetaSlugs.BLACKLISTED_BALANCE,
        payload={"balance": total_balance},
        updated_at=datetime.now()
    )
    await MetaCRUD.update_or_insert(
        {"slug": MetaSlugs.BLACKLISTED_BALANCE}, meta_instance.dict()
    )
    logging.info(f"Updated blacklisted balance: {total_balance}")
    return
