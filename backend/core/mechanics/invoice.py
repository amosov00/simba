from typing import Union, List, Tuple, Optional
from http import HTTPStatus
from datetime import datetime

from fastapi import HTTPException
from sentry_sdk import capture_message

from .crypto import SimbaWrapper
from .crypto.base import CryptoValidation
from database.crud import BTCTransactionCRUD, InvoiceCRUD
from core.mechanics.crypto.sst import SSTWrapper
from database.crud import UserCRUD
from schemas import (
    InvoiceInDB,
    InvoiceType,
    InvoiceStatus,
    EthereumTransaction,
    BTCTransaction,
    BTCTransactionOutputs,
    BTCTransactionInDB,
)
from config import BTC_MINIMAL_CONFIRMATIONS


class InvoiceMechanics(CryptoValidation):
    def __init__(self, invoice: Union[dict, InvoiceInDB]):
        if isinstance(invoice, dict):
            invoice = InvoiceInDB(**invoice)

        self.invoice = invoice
        self.errors = []

    def _raise_exception_if_exists(self):
        if self.errors:
            raise HTTPException(HTTPStatus.BAD_REQUEST, self.errors)
        else:
            return None

    def _validate_common(self):
        if not self.invoice.user_id:
            self.errors.append("`user_id` field is missing")

        return None

    def _validate_for_buy(self):
        if not self.invoice.target_btc_address:
            self.errors.append("bitcoin wallet address is required")
        if not self.invoice.target_eth_address:
            self.errors.append("ethereum wallet address is required")
        if not self.validate_simba_amount(self.invoice.simba_amount):
            self.errors.append(f"min simba token amount: {self.SIMBA_TOKENS_MINIMAL_AMOUNT}")
        if not self.validate_currency_rate(self.invoice.btc_amount, self.invoice.simba_amount):
            self.errors.append("invalid rate")

        # TODO fields:
        return True

    def _validate_for_sell(self):
        # TODO fill
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
            cls,
            outputs: List[BTCTransactionOutputs],
            target_btc_address: str
    ) -> Optional[int]:
        incoming_btc = None

        res = list(filter(lambda o: target_btc_address in o.addresses, outputs))

        if res:
            res = res[0]
            incoming_btc = res.value

        return incoming_btc

    async def _issue_simba_tokens_and_save(
            self,
            transaction: BTCTransaction,
            incoming_btc: int,
    ):
        self._raise_exception_if_exists()
        eth_tx_hash = await SimbaWrapper().issue_tokens(
            self.invoice.target_eth_address, incoming_btc=incoming_btc, comment=transaction.hash
        )
        transaction.simba_tokens_issued = True
        await BTCTransactionCRUD.update_or_insert({"hash": transaction.hash}, transaction.dict())
        self.invoice.status = InvoiceStatus.COMPLETED
        self.invoice.btc_amount_proceeded += incoming_btc
        self.invoice.finised_at = datetime.now()

        await self.update_invoice()
        sst_w = SSTWrapper()
        user = UserCRUD.find_by_id(self.invoice.user_id)
        sst_w.send_sst_to_referrals(user, self.invoice.btc_amount)
        # TODO: Call method which issue SST tokens (Try to call it without celery) (invomcing btc == simba )
        return True

    async def proceed_new_btc_transaction(
            self,
            transaction: BTCTransaction,
            **kwargs
    ):
        if transaction.block_height < 0 or transaction.confirmations == 0:
            self.errors.append("transaction is not confirmed yet")

        transaction.invoice_id = self.invoice.id
        incoming_btc = self.get_incoming_btc_from_outputs(transaction.outputs, self.invoice.target_btc_address)

        if not incoming_btc:
            self.errors.append("Failed to parse btc amount from transaction")

        if transaction_in_db := await BTCTransactionCRUD.find_one({
            "hash": transaction.hash,
        }):
            transaction_in_db = BTCTransactionInDB(**transaction_in_db)

        self._raise_exception_if_exists()

        if transaction_in_db:
            if transaction.confirmations < BTC_MINIMAL_CONFIRMATIONS:
                await BTCTransactionCRUD.update_or_insert({"hash": transaction.hash}, transaction.dict())

            elif transaction.confirmations >= BTC_MINIMAL_CONFIRMATIONS and transaction_in_db.simba_tokens_issued:
                self.errors.append("transaction already exists and simba tokens was issued")
                self._raise_exception_if_exists()
                await BTCTransactionCRUD.update_one({"hash": transaction.hash}, transaction.dict())

            elif transaction.confirmations >= BTC_MINIMAL_CONFIRMATIONS and not transaction_in_db.simba_tokens_issued:
                return await self._issue_simba_tokens_and_save(transaction, incoming_btc)

        else:
            if transaction.confirmations < BTC_MINIMAL_CONFIRMATIONS:
                await BTCTransactionCRUD.update_or_insert({"hash": transaction.hash}, transaction.dict())

            elif transaction.confirmations >= BTC_MINIMAL_CONFIRMATIONS:
                return await self._issue_simba_tokens_and_save(transaction, incoming_btc)

        return True

    async def proceed_new_eth_transaction(
            self,
            transaction: EthereumTransaction,
            **kwargs
    ):
        print("DEBUG BELOW")
        print(transaction)
        print(kwargs)
        return False

    async def proceed_new_transaction(
            self,
            transaction: Union[BTCTransaction, EthereumTransaction],
            **kwargs
    ) -> Union[bool, str]:
        if isinstance(transaction, BTCTransaction):
            return await self.proceed_new_btc_transaction(transaction, **kwargs)
        elif isinstance(transaction, EthereumTransaction):
            return await self.proceed_new_eth_transaction(transaction, **kwargs)

    async def update_invoice(self):
        return await InvoiceCRUD.update_one({"_id": self.invoice.id}, self.invoice.dict(exclude={'id'}))
