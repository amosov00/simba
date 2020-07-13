from celery_app.celeryconfig import app
from database.crud import InvoiceCRUD, EthereumTransactionCRUD, UserCRUD
from schemas import SSTContractEvents, EthereumTransactionInDB, InvoiceStatus, InvoiceType
from core.integrations.ethereum import EventsContractWrapper
from core.mechanics import InvoiceMechanics
from config import SST_CONTRACT, SST_ADMIN_ADDRESS

__all__ = ["fetch_and_proceed_sst_contract_cronjob"]


@app.task(
    name="fetch_and_proceed_sst_contract", bind=True, soft_time_limit=42, time_limit=300,
)
async def fetch_and_proceed_sst_contract_cronjob(self, *args, **kwargs):
    await EventsContractWrapper(SST_CONTRACT).fetch_blocks_and_save()

    transactions = await EthereumTransactionCRUD.find(
        {
            "contract": SST_CONTRACT.title,
            "event": SSTContractEvents.Transfer,
            "user_id": None,
            "args.from": {"$regex": SST_ADMIN_ADDRESS, "$options": "i"},
        }
    )

    for transaction in transactions:
        address_to = transaction["args"].get("to")

        user = await UserCRUD.find_one({
            "user_eth_addresses.address": {"$regex": address_to, "$options": "i"}
        })

        if user:
            await EthereumTransactionCRUD.update_one(
                {"_id": transaction["_id"]}, {"user_id": user["_id"]}
            )

    return True
