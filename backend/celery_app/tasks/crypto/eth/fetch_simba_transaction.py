from database.crud import InvoiceCRUD, EthereumTransactionCRUD
from schemas import InvoiceInDB, SimbaContractEvents, EthereumTransaction
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
    # TODO Complete
    await ContractEventsWrapper(SIMBA_CONTRACT).fetch_blocks_and_save()

    transactions = await EthereumTransactionCRUD.find({
        "event": {"$in": SimbaContractEvents.ALL},
        "invoice_id": None,
    })
    for transaction in transactions:
        transaction = EthereumTransaction(**transaction)
        invoice = await InvoiceCRUD.find_one({
            "target_eth_address": transaction.address,
        })
        if invoice:
            transaction.invoice_id = invoice["_id"]
            await EthereumTransactionCRUD.update_one({
                "transactionHash": transaction.transactionHash,
                "event": transaction.event,
                "logIndex": transaction.logIndex,
            }, transaction.dict())

    return True
