import logging
from datetime import timedelta

from config import SST_CONTRACT, settings
from core.integrations.ethereum import EventsContractWrapper
from database.crud import EthereumTransactionCRUD, UserCRUD, InvoiceCRUD
from schemas import SSTContractEvents
from workers.agents import app

__all__ = ["fetch_and_proceed_sst_contract_job"]

fetch_and_proceed_sst_contract_topic = app.topic(
    "fetch_and_proceed_sst_contract", internal=True, retention=timedelta(minutes=10), partitions=1
)


@app.agent(fetch_and_proceed_sst_contract_topic, concurrency=1)
async def fetch_and_proceed_sst_contract_job(stream):
    """Синхронизация с SST контрактом."""
    async for _ in stream:
        await EventsContractWrapper(SST_CONTRACT).fetch_blocks_and_save()

        transactions = await EthereumTransactionCRUD.find(
            {
                "$and": [
                    {"contract": SST_CONTRACT.title},
                    {"event": SSTContractEvents.Transfer},
                    {"args.from": {"$regex": settings.crypto.simba_admin_address, "$options": "i"}},
                    {"$or": [{"user_id": None}, {"invoice_id": None}]},
                ]
            }
        )
        logging.info(f"SST TX to proceed: {len(transactions)}")

        for transaction in transactions:
            tx_hash = transaction["transactionHash"]
            address_to = transaction["args"].get("to")

            user = await UserCRUD.find_one({"user_eth_addresses.address": {"$regex": address_to, "$options": "i"}})

            if user:
                await EthereumTransactionCRUD.update_one({"_id": transaction["_id"]}, {"user_id": user["_id"]})

            if invoice := await InvoiceCRUD.find_one({"sst_tx_hashes": tx_hash}):
                await EthereumTransactionCRUD.update_one({"_id": transaction["_id"]}, {"invoice_id": invoice["_id"]})

    return True
