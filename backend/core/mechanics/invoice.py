import asyncio, logging
from typing import Union, List, Tuple, Optional
from http import HTTPStatus
from datetime import datetime

from fastapi import HTTPException
from sentry_sdk import capture_message

from database.crud import BTCTransactionCRUD, InvoiceCRUD, EthereumTransactionCRUD
from core.mechanics.crypto import SSTWrapper, SimbaWrapper, BitcoinWrapper
from core.mechanics.crypto.base import CryptoValidation
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
    SimbaContractEvents
)
from config import BTC_MINIMAL_CONFIRMATIONS


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
            self.errors.append(f"min simba token amount: {self.SIMBA_TOKENS_MINIMAL_AMOUNT}")
        if not self.validate_currency_rate(self.invoice.btc_amount, self.invoice.simba_amount):
            self.errors.append("invalid rate")
        if self.invoice.invoice_type not in (InvoiceType.SELL, InvoiceType.BUY):
            self.errors.append("invalid invoice type")

        return None

    def _validate_for_buy(self):
        if self.user:
            if not self.user.has_address("eth", self.invoice.target_eth_address):
                self.errors.append("user has no target_eth_address")
        return True

    def _validate_for_sell(self):
        if self.user:
            if not self.user.has_address("eth", self.invoice.target_eth_address):
                self.errors.append("user has no target_eth_address")
            if not self.user.has_address("btc", self.invoice.target_btc_address):
                self.errors.append("user has no target_btc_address")
        return True

    def _validate_for_sending_btc(self):
        if not self.invoice.status == InvoiceStatus.PROCESSING:
            self.errors.append("invalid invoice status")
        if self.invoice.simba_amount_proceeded < self.SIMBA_BUY_SELL_FEE:
            self.errors.append("too low simba tokens value")

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

        if transaction.event == SimbaContractEvents.Transfer:
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
        # Incoming BTC - fee (50000)
        self.invoice.simba_amount_proceeded += incoming_btc - 50000
        self.invoice.add_hash("eth", eth_tx_hash)
        self.invoice.add_hash("btc", transaction.hash)

        await self.update_invoice()
        user = await UserCRUD.find_by_id(self.invoice.user_id)
        user = User(**user)
        asyncio.create_task(SSTWrapper().send_sst_to_referrals(user, self.invoice.btc_amount))
        return True

    async def proceed_new_btc_transaction(self, transaction: BTCTransaction):
        if transaction.block_height < 0 or transaction.confirmations == 0:
            self.errors.append("transaction is not confirmed yet")

        transaction.invoice_id = self.invoice.id
        transaction.user_id = self.user.id if self.user else self.invoice.user_id

        incoming_btc = self.get_incoming_btc_from_outputs(transaction.outputs, self.invoice.target_btc_address)

        if not incoming_btc:
            self.errors.append("Failed to parse btc amount from transaction")

        if transaction_in_db := await BTCTransactionCRUD.find_one({"hash": transaction.hash, }):
            transaction_in_db = BTCTransactionInDB(**transaction_in_db)

        self._raise_exception_if_exists()

        if transaction_in_db:
            if transaction.confirmations < BTC_MINIMAL_CONFIRMATIONS:
                await BTCTransactionCRUD.update_or_insert({"hash": transaction.hash}, transaction.dict())

            elif (
                    transaction.confirmations >= BTC_MINIMAL_CONFIRMATIONS and transaction_in_db.simba_tokens_issued
            ):
                self.errors.append("transaction already exists and simba tokens was issued")
                self._raise_exception_if_exists()
                await BTCTransactionCRUD.update_one({"hash": transaction.hash}, transaction.dict())

            elif (
                    transaction.confirmations >= BTC_MINIMAL_CONFIRMATIONS
                    and not transaction_in_db.simba_tokens_issued
            ):
                return await self._issue_simba_tokens_and_save(transaction, incoming_btc)

        else:
            if transaction.confirmations < BTC_MINIMAL_CONFIRMATIONS:
                await BTCTransactionCRUD.update_or_insert({"hash": transaction.hash}, transaction.dict())

            elif transaction.confirmations >= BTC_MINIMAL_CONFIRMATIONS:
                return await self._issue_simba_tokens_and_save(transaction, incoming_btc)

        return True

    async def proceed_new_eth_transaction(self, transaction: Union[EthereumTransaction, EthereumTransactionInDB]):
        logging.info(f"TX:{transaction}\nINV:{self.invoice.id}")
        incoming_eth = self.get_incoming_simba(transaction)

        if not incoming_eth:
            capture_message("failed to parse incoming eth from transaction", level="error")
            self.errors.append("failed to parse incoming eth from transaction")

        self._raise_exception_if_exists()

        transaction.invoice_id = self.invoice.id
        transaction.bitcoins_sended = True
        transaction.user_id = self.user.id if self.user else None

        self.invoice.status = InvoiceStatus.PROCESSING
        self.invoice.simba_amount_proceeded = incoming_eth
        self.invoice.add_hash("eth", transaction.transactionHash)

        await EthereumTransactionCRUD.update_one({"_id": transaction.id}, transaction.dict(exclude={"id"}))
        await self.update_invoice()
        return True

    async def proceed_new_transaction(
            self, transaction: Union[BTCTransaction, EthereumTransaction], **kwargs
    ) -> Union[bool, str]:
        if isinstance(transaction, BTCTransaction) or isinstance(transaction, BTCTransactionInDB):
            return await self.proceed_new_btc_transaction(transaction)
        elif isinstance(transaction, EthereumTransaction) or isinstance(transaction, EthereumTransactionInDB):
            return await self.proceed_new_eth_transaction(transaction)

    async def update_invoice(self):
        return await InvoiceCRUD.update_one({"_id": self.invoice.id}, self.invoice.dict(exclude={"id"}))

    async def send_bitcoins(self):
        self._validate_for_sending_btc()

        btc_outcoming = self.invoice.simba_amount_proceeded

        btc_tx = await BitcoinWrapper().create_and_sign_transaction(
            address=self.invoice.target_btc_address, amount=btc_outcoming
        )
        eth_tx_hash = await SimbaWrapper().redeem_tokens(
            btc_outcoming, btc_tx.hash
        )
        btc_tx.simba_tokens_issued = True
        btc_tx.invoice_id = self.invoice.id

        self.invoice.btc_amount_proceeded = btc_outcoming
        self.invoice.status = InvoiceStatus.COMPLETED
        self.invoice.add_hash("eth", eth_tx_hash)
        self.invoice.add_hash("btc", btc_tx.hash)

        await BTCTransactionCRUD.insert_one(btc_tx.dict())
        await self.update_invoice()
        return True
