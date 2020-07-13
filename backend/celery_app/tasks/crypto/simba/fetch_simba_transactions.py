from celery_app.celeryconfig import app
from database.crud import InvoiceCRUD, EthereumTransactionCRUD, UserCRUD
from schemas import SimbaContractEvents, EthereumTransactionInDB, InvoiceStatus, InvoiceType
from core.integrations.ethereum import EventsContractWrapper
from core.mechanics import InvoiceMechanics
from config import SIMBA_CONTRACT, SIMBA_ADMIN_ADDRESS

__all__ = ["fetch_and_proceed_simba_contract"]


@app.task(
    name="fetch_and_proceed_simba_contract", bind=True, soft_time_limit=42, time_limit=300,
)
async def fetch_and_proceed_simba_contract(self, *args, **kwargs):
    """Синхронизация с Simba контрактом"""
    await EventsContractWrapper(SIMBA_CONTRACT).fetch_blocks_and_save()

    transactions = await EthereumTransactionCRUD.find(
        {"contract": SIMBA_CONTRACT.title, "event": {"$in": SimbaContractEvents.ALL}, "invoice_id": None}
    )
    for transaction in transactions:
        transaction = EthereumTransactionInDB(**transaction)

        if transaction.event == SimbaContractEvents.Transfer:
            # Connect with sell invoices
            sender_hash = transaction.args.get("from")
            receiver_hash = transaction.args.get("to")

            if not SIMBA_ADMIN_ADDRESS.lower() == receiver_hash.lower():
                continue

            invoice = await InvoiceCRUD.find_one(
                {
                    "status": InvoiceStatus.WAITING,
                    "invoice_type": InvoiceType.SELL,
                    "target_eth_address": {"$regex": sender_hash, "$options": "i"},
                    "created_at": {"$lte": transaction.fetched_at}
                }
            ) if sender_hash else None

            if invoice:
                user = await UserCRUD.find_by_id(invoice["user_id"])
                await InvoiceMechanics(invoice, user).proceed_new_transaction(transaction)
            else:
                continue

        elif transaction.event in (SimbaContractEvents.OnRedeemed, SimbaContractEvents.OnIssued):
            # Connect with finished invoices
            # TODO Complete
            pass

    return True
