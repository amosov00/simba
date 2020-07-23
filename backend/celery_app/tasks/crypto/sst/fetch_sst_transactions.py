import logging

from celery_app.celeryconfig import app
from config import SST_CONTRACT, SST_ADMIN_ADDRESS
from core.integrations.ethereum import EventsContractWrapper
from database.crud import EthereumTransactionCRUD, UserCRUD, InvoiceCRUD
from schemas import SSTContractEvents

__all__ = ["fetch_and_proceed_sst_contract"]


@app.task(
    name="fetch_and_proceed_sst_contract", bind=True, soft_time_limit=42, time_limit=300,
)
async def fetch_and_proceed_sst_contract(self, *args, **kwargs):
    """Синхронизация с SST контрактом"""
    await EventsContractWrapper(SST_CONTRACT).fetch_blocks_and_save()

    transactions = await EthereumTransactionCRUD.find(
        {
            "contract": SST_CONTRACT.title,
            "event": SSTContractEvents.Transfer,
            "user_id": None,
            "args.from": {"$regex": SST_ADMIN_ADDRESS, "$options": "i"},
        }
    )
    logging.info(f"SST TX to proceed: {len(transactions)}")

    for transaction in transactions:
        tx_hash = transaction["transactionHash"]
        address_to = transaction["args"].get("to")

        user = await UserCRUD.find_one({"user_eth_addresses.address": {"$regex": address_to, "$options": "i"}})

        if user:
            await EthereumTransactionCRUD.update_one(
                {"_id": transaction["_id"]},
                {"user_id": user["_id"]}
            )

        elif invoice := await InvoiceCRUD.find_one({"sst_tx_hashes": tx_hash}):
            await EthereumTransactionCRUD.update_one(
                {"_id": transaction["_id"]},
                {"user_id": invoice["user_id"]}
            )

    return True
