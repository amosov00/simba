import asyncio
import logging
from datetime import datetime
from http import HTTPStatus
from typing import Union, List, Optional

from fastapi import HTTPException
from sentry_sdk import capture_message

from config import TRANSACTION_MIN_CONFIRMATIONS
from core.mechanics import SimbaWrapper, SSTWrapper, BitcoinWrapper, BlockCypherWebhookHandler
from core.mechanics.crypto.base import CryptoValidation
from database.crud import BTCTransactionCRUD, InvoiceCRUD, EthereumTransactionCRUD
from database.crud import UserCRUD
from schemas import (
    User,
    InvoiceInDB,
    InvoiceType,
    InvoiceStatus,
    EthereumTransaction,
    EthereumTransactionInDB,
    BTCTransaction,
    BTCTransactionOutputs,
    BTCTransactionInDB,
    SimbaContractEvents,
    BlockCypherWebhookEvents,
)
from config import SIMBA_BUY_SELL_FEE, SIMBA_MINIMAL_BUY_AMOUNT


class InvoiceMechanics(CryptoValidation):
    def __init__(self, invoice: Union[dict, InvoiceInDB], user: Union[dict, User] = None):
        if isinstance(invoice, dict):
            invoice = InvoiceInDB(**invoice)

        if user and isinstance(user, dict):
            user = User(**user)

        self.invoice = invoice
        self.user = user
        self.errors = []

    def _raise_exception_if_exists(self):
        if self.errors:
            raise HTTPException(HTTPStatus.BAD_REQUEST, self.errors)
        else:
            return None

    def _validate_common(self):
        if not self.invoice.user_id:
            self.errors.append("`user_id` field is missing")
        if not self.invoice.target_btc_address:
            self.errors.append("bitcoin wallet address is required")
        if not self.invoice.target_eth_address:
            self.errors.append("ethereum wallet address is required")
        if not self.validate_simba_amount(self.invoice.simba_amount):
            self.errors.append(f"min simba token amount: {SIMBA_MINIMAL_BUY_AMOUNT}")
        if self.invoice.invoice_type not in (InvoiceType.SELL, InvoiceType.BUY):
            self.errors.append("invalid invoice type")

        return None

    def _validate_for_buy(self):
        if not self.validate_currency_rate(
                self.invoice.invoice_type, self.invoice.btc_amount, self.invoice.simba_amount
        ):
            self.errors.append("invalid rate")
        if self.user:
            if not self.user.has_address("eth", self.invoice.target_eth_address):
                self.errors.append("user has no target_eth_address")
        return True

    def _validate_for_sell(self):
        if not self.validate_currency_rate(
                self.invoice.invoice_type, self.invoice.btc_amount, self.invoice.simba_amount
        ):
            self.errors.append("invalid rate")
        if self.user:
            if not self.user.has_address("eth", self.invoice.target_eth_address):
                self.errors.append("user has no target_eth_address")
            if not self.user.has_address("btc", self.invoice.target_btc_address):
                self.errors.append("user has no target_btc_address")
        return True

    def _validate_for_sending_btc(self):
        if not self.invoice.status == InvoiceStatus.PROCESSING:
            self.errors.append("invalid invoice status")
        if self.invoice.simba_amount_proceeded < SIMBA_MINIMAL_BUY_AMOUNT:
            self.errors.append("too low simba tokens value")
        if self.invoice.simba_amount_proceeded == self.invoice.btc_amount_proceeded + SIMBA_BUY_SELL_FEE:
            self.errors.append("btc are already sent")
        if self.invoice.btc_tx_hashes:
            self.errors.append("btc txs are already exist")

        self._raise_exception_if_exists()

        return True

    def validate(self) -> bool:
        self._validate_common()

        if self.invoice.invoice_type == InvoiceType.BUY:
            self._validate_for_buy()

        elif self.invoice.invoice_type == InvoiceType.SELL:
            self._validate_for_sell()

        self._raise_exception_if_exists()

        return True

    @classmethod
    def get_incoming_btc_from_outputs(
            cls, outputs: List[BTCTransactionOutputs], target_btc_address: str
    ) -> Optional[int]:
        incoming_btc = None

        res = list(filter(lambda o: target_btc_address in o.addresses, outputs))

        if res:
            res = res[0]
            incoming_btc = res.value

        return incoming_btc

    @classmethod
    def get_incoming_simba(cls, transaction: Union[EthereumTransaction, EthereumTransactionInDB]) -> int:
        value = 0

        if transaction.event in SimbaContractEvents.ALL:
            value = transaction.args.get("value")

        return value

    async def _issue_simba_tokens_and_save(
            self, transaction: BTCTransaction, incoming_btc: int,
    ):
        self._raise_exception_if_exists()
        eth_tx_hash = await SimbaWrapper().issue_tokens(
            self.invoice.target_eth_address, incoming_btc=incoming_btc, btc_tx_hash=transaction.hash
        )
        transaction.simba_tokens_issued = True
        await BTCTransactionCRUD.update_or_insert({"hash": transaction.hash}, transaction.dict())
        self.invoice.status = InvoiceStatus.COMPLETED
        self.invoice.finised_at = datetime.now()
        self.invoice.btc_amount_proceeded += incoming_btc
        # Subtract fee
        self.invoice.simba_amount_proceeded += incoming_btc - SIMBA_BUY_SELL_FEE
        self.invoice.add_hash("eth", eth_tx_hash)
        self.invoice.add_hash("btc", transaction.hash)

        await self.update_invoice()
        user = await UserCRUD.find_by_id(self.invoice.user_id)
        user = User(**user)
        asyncio.create_task(SSTWrapper().send_sst_to_referrals(user, self.invoice.btc_amount))
        return True

    async def _proceed_new_btc_tx_buy(
            self, new_transaction: BTCTransaction, transaction_in_db: BTCTransactionInDB
    ):
        """Part of buy pipeline"""
        incoming_btc = self.get_incoming_btc_from_outputs(
            new_transaction.outputs, self.invoice.target_btc_address
        )

        if not incoming_btc:
            capture_message("Failed to parse btc amount from transaction", level="error")
            self.errors.append("Failed to parse btc amount from transaction")
            self._raise_exception_if_exists()

        if all([
            bool(new_transaction.block_height),
            new_transaction.confirmations >= TRANSACTION_MIN_CONFIRMATIONS,
            transaction_in_db.simba_tokens_issued is False if transaction_in_db else True,
            self.invoice.status == InvoiceStatus.WAITING
        ]):
            return await self._issue_simba_tokens_and_save(new_transaction, incoming_btc)

        else:
            return await BTCTransactionCRUD.update_or_insert(
                {"hash": new_transaction.hash}, new_transaction.dict(exclude_unset=True)
            )

    async def _proceed_new_btc_tx_sell(self, new_transaction: BTCTransaction, transaction_in_db: BTCTransactionInDB):
        """Part of sell pipeline"""
        if all([
            bool(new_transaction.block_height),
            new_transaction.confirmations >= TRANSACTION_MIN_CONFIRMATIONS,
            transaction_in_db.simba_tokens_issued is False if transaction_in_db else True,
            self.invoice.status == InvoiceStatus.PROCESSING
        ]):

            self.invoice.status = InvoiceStatus.COMPLETED
            self.invoice.finised_at = datetime.now()

            # send without fee cause of double fee charge
            btc_outcoming_without_fee = self.invoice.btc_amount_proceeded + SIMBA_BUY_SELL_FEE

            eth_tx_hash = await SimbaWrapper().redeem_tokens(
                btc_outcoming_without_fee,
                new_transaction.hash
            )
            self.invoice.add_hash("eth", eth_tx_hash)

            await self.update_invoice()
            await BTCTransactionCRUD.update_or_insert(
                {"hash": new_transaction.hash}, new_transaction.dict(exclude_unset=True)
            )

        else:
            await BTCTransactionCRUD.update_or_insert(
                {"hash": new_transaction.hash}, new_transaction.dict(exclude_unset=True)
            )

        return True

    async def proceed_new_btc_transaction(self, transaction: BTCTransaction):
        transaction.invoice_id = self.invoice.id

        if transaction_in_db := await BTCTransactionCRUD.find_one({"hash": transaction.hash}):
            transaction_in_db = BTCTransactionInDB(**transaction_in_db)

        self._raise_exception_if_exists()

        if self.invoice.invoice_type == InvoiceType.BUY:
            return await self._proceed_new_btc_tx_buy(transaction, transaction_in_db)

        elif self.invoice.invoice_type == InvoiceType.SELL:
            return await self._proceed_new_btc_tx_sell(transaction, transaction_in_db)

        return True

    async def _proceed_new_eth_tx_transfer(self, transaction: EthereumTransactionInDB):
        """Part of sell pipeline"""
        incoming_eth = self.get_incoming_simba(transaction)

        if not incoming_eth:
            capture_message("failed to parse incoming eth from transaction", level="error")
            self.errors.append("failed to parse incoming eth from transaction")

        if not self.invoice.status == InvoiceStatus.WAITING:
            capture_message("invalid invoice status in sell invoice pipeline", level="error")
            self.errors.append("invalid invoice status in sell invoice pipeline")

        self._raise_exception_if_exists()

        transaction.invoice_id = self.invoice.id
        transaction.bitcoins_sended = True  # TODO is it correct ?

        self.invoice.status = InvoiceStatus.PROCESSING
        self.invoice.simba_amount_proceeded = incoming_eth
        self.invoice.add_hash("eth", transaction.transactionHash)

        await EthereumTransactionCRUD.update_one({"_id": transaction.id}, transaction.dict(exclude={"id"}))
        await self.update_invoice()
        return True

    async def _proceed_new_eth_tx_issue_redeem(self, transaction: EthereumTransactionInDB):
        """Part of buy and sell pipeline, just for adding extra info in invoice"""
        transaction.invoice_id = self.invoice.id
        self.invoice.add_hash("eth", transaction.transactionHash)

        await EthereumTransactionCRUD.update_one({"_id": transaction.id}, transaction.dict(exclude={"id"}))
        await self.update_invoice()
        return True

    async def proceed_new_eth_transaction(self, transaction: EthereumTransactionInDB):
        if transaction.event == SimbaContractEvents.Transfer:
            return await self._proceed_new_eth_tx_transfer(transaction)
        elif transaction.event in (SimbaContractEvents.OnRedeemed, SimbaContractEvents.OnIssued):
            return await self._proceed_new_eth_tx_issue_redeem(transaction)
        else:
            capture_message("Unindentified invoice type", level="warning")
        return True

    async def proceed_new_transaction(
            self, transaction: Union[BTCTransaction, EthereumTransaction], **kwargs
    ) -> Union[bool, str]:
        if isinstance(transaction, (BTCTransaction, BTCTransactionInDB)):
            return await self.proceed_new_btc_transaction(transaction)
        elif isinstance(transaction, (EthereumTransaction, EthereumTransactionInDB)):
            return await self.proceed_new_eth_transaction(transaction)

    async def update_invoice(self):
        return await InvoiceCRUD.update_one({"_id": self.invoice.id}, self.invoice.dict(exclude={"id"}))

    async def send_bitcoins(self):
        self._validate_for_sending_btc()

        btc_outcoming_without_fee = self.invoice.simba_amount_proceeded
        btc_outcoming_with_fee = btc_outcoming_without_fee - SIMBA_BUY_SELL_FEE

        btc_tx = await BitcoinWrapper().create_and_sign_transaction(
            address=self.invoice.target_btc_address, amount=btc_outcoming_with_fee
        )
        if not btc_tx:
            capture_message(f"failed to get btc tx info from invoice {self.invoice.id}", level="error")
            return False

        btc_tx.invoice_id = self.invoice.id
        self.invoice.btc_amount_proceeded = btc_outcoming_with_fee
        self.invoice.add_hash("btc", btc_tx.hash)

        await BTCTransactionCRUD.insert_one(btc_tx.dict())
        await self.update_invoice()

        asyncio.create_task(
            BlockCypherWebhookHandler().create_webhook(
                invoice=self.invoice,
                event=BlockCypherWebhookEvents.TX_CONFIMATION,
                transaction_hash=btc_tx.hash,
            )
        )
        return True
