import asyncio
import re

from celery_app.celeryconfig import app
from database.crud import InvoiceCRUD, EthereumTransactionCRUD
from schemas import SimbaContractEvents, EthereumTransactionInDB
from core.integrations.ethereum import EventsContractWrapper
from core.mechanics import InvoiceMechanics
from config import SIMBA_CONTRACT, SIMBA_ADMIN_ADDRESS

__all__ = ["fetch_simba_contract_cronjob"]


@app.task(
    name="fetch_simba_contract", bind=True, soft_time_limit=42, time_limit=300,
)
async def fetch_simba_contract_cronjob(self, *args, **kwargs):
    # TODO Complete
    await EventsContractWrapper(SIMBA_CONTRACT).fetch_blocks_and_save()

    transactions = await EthereumTransactionCRUD.find(
        {"event": {"$in": SimbaContractEvents.ALL}, "invoice_id": None}
    )
    for transaction in transactions:
        transaction = EthereumTransactionInDB(**transaction)

        if transaction.event == SimbaContractEvents.Transfer:
            sender_hash = transaction.args.get("from")
            receiver_hash = transaction.args.get("to")
            invoice = await InvoiceCRUD.find_one(
                {"target_eth_address": {"$regex": sender_hash, "$options": "i"}}
            ) if sender_hash else None

            if invoice and SIMBA_ADMIN_ADDRESS.lower() == receiver_hash.lower():
                await InvoiceMechanics(invoice).proceed_new_transaction(transaction)
            else:
                continue

        elif transaction.event in (SimbaContractEvents.OnRedeemed, SimbaContractEvents.OnIssued):
            # Connect with finished invoices
            invoice = await InvoiceCRUD.find_one({"target_eth_address": transaction.address})
            pass

    # TODO: On issue - save invoice_id to ETHTrans
    # TODO: On redeem - save invoice_id and gen btc on
    return True
