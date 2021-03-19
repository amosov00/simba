import logging
from datetime import datetime, timedelta

from bson import Decimal128

from config import SIMBA_CONTRACT, settings
from core.integrations.ethereum import EventsContractWrapper
from core.mechanics.invoices import InvoiceMechanics
from database.crud import InvoiceCRUD, EthereumTransactionCRUD, UserCRUD
from schemas import SimbaContractEvents, EthereumTransactionInDB, InvoiceStatus, InvoiceType
from workers.agents import app

__all__ = ["fetch_and_proceed_simba_contract_job"]

fetch_and_proceed_simba_contract_topic = app.topic(
    "fetch_and_proceed_simba_contract", internal=True, retention=timedelta(minutes=10), partitions=1
)


@app.agent(fetch_and_proceed_simba_contract_topic, concurrency=1)
async def fetch_and_proceed_simba_contract_job(stream):
    """Синхронизация с Simba контрактом."""
    async for _ in stream:
        await EventsContractWrapper(SIMBA_CONTRACT).fetch_blocks_and_save()
        counter = 0
        transactions = await EthereumTransactionCRUD.find(
            {
                "contract": SIMBA_CONTRACT.title,
                "event": {"$in": SimbaContractEvents.ALL},
                "invoice_id": None,
                "skip": {"$ne": True},
            }
        )

        logging.info(f"Simba TX to proceed: {len(transactions)}")

        for transaction in transactions:
            transaction = EthereumTransactionInDB(**transaction)

            if transaction.event == SimbaContractEvents.Transfer:
                # Connect with sell invoices
                sender_hash = transaction.args.get("from")
                receiver_hash = transaction.args.get("to")

                if all(
                    [
                        transaction.event == SimbaContractEvents.Transfer,
                        settings.crypto.simba_admin_address.lower() != receiver_hash.lower(),
                        settings.crypto.simba_admin_address.lower() != sender_hash.lower(),
                    ]
                ):
                    # Mark transaction as service
                    transaction.skip = True
                    await EthereumTransactionCRUD.update_one({"_id": transaction.id}, transaction.dict(exclude={"id"}))
                    continue

                invoice = await InvoiceCRUD.find_one(
                    {
                        "$or": [
                            {
                                "status": InvoiceStatus.WAITING,
                                "invoice_type": InvoiceType.SELL,
                                "target_eth_address": {"$regex": sender_hash, "$options": "i"},
                                "created_at": {"$lte": transaction.fetched_at},
                            },
                            {"invoice_type": InvoiceType.SELL, "eth_tx_hashes": transaction.transactionHash},
                        ]
                    }
                )

                if invoice:
                    counter += 1
                    user = await UserCRUD.find_by_id(invoice["user_id"])
                    await InvoiceMechanics(invoice, user).proceed_new_transaction(transaction)
                else:
                    pass

            elif transaction.event in (SimbaContractEvents.OnIssued, SimbaContractEvents.OnRedeemed):
                customer_address = transaction.args.get("customerAddress")
                timestamp = transaction.args.get("timestamp")
                if timestamp and isinstance(timestamp, Decimal128):
                    timestamp = int(timestamp.to_decimal())

                tx_datetime = datetime.fromtimestamp(timestamp)
                btc_tx_hash = transaction.args.get("comment")
                invoice_type = (
                    InvoiceType.BUY if transaction.event == SimbaContractEvents.OnIssued else InvoiceType.SELL
                )

                invoice = await InvoiceCRUD.find_one(
                    {
                        "$or": [
                            {
                                "status": InvoiceStatus.COMPLETED,
                                "invoice_type": invoice_type,
                                "target_eth_address": {"$regex": customer_address, "$options": "i"},
                                "created_at": {"$lte": tx_datetime},
                                "btc_tx_hashes": btc_tx_hash,
                            },
                            {
                                "invoice_type": invoice_type,
                                "eth_tx_hashes": transaction.transactionHash,
                            },
                        ]
                    }
                )

                if invoice:
                    counter += 1
                    await InvoiceMechanics(invoice).proceed_new_transaction(transaction)
                else:
                    pass

            elif transaction.event in (SimbaContractEvents.BlacklistedAdded, SimbaContractEvents.BlacklistedRemoved):
                transaction.skip = True
                await EthereumTransactionCRUD.update_one({"_id": transaction.id}, {"skip": transaction.skip})
                counter += 1

        if counter:
            logging.info(f"Proceeded new {counter} simba transactions")

    return
