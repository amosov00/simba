from typing import Union
from http import HTTPStatus
from datetime import datetime

from fastapi import HTTPException

from .crypto import SimbaWrapper
from .crypto.base import CryptoValidation
from database.crud import BTCTransactionCRUD, InvoiceCRUD
from schemas import (
    InvoiceInDB,
    InvoiceType,
    InvoiceStatus,
    EthereumTransaction,
    BTCTransaction,
    BTCTransactionInDB,
)


class InvoiceMechanics(CryptoValidation):
    def __init__(self, invoice: Union[dict, InvoiceInDB]):
        if isinstance(invoice, dict):
            invoice = InvoiceInDB(**invoice)

        self.invoice = invoice
        self.errors = []

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

    def validate(self) -> InvoiceInDB:
        self._validate_common()

        if self.invoice.invoice_type == InvoiceType.BUY:
            self._validate_for_buy()

        elif self.invoice.invoice_type == InvoiceType.SELL:
            self._validate_for_sell()

        if self.errors:
            raise HTTPException(HTTPStatus.BAD_REQUEST, self.errors)

        return self.invoice

    async def update_invoice(self):
        return await InvoiceCRUD.update_one({"_id": self.invoice.id}, self.invoice.dict(exclude={'id'}))

    async def proceed_new_btc_transaction(
            self,
            transaction: BTCTransaction,
            incoming_btc: int,
            raise_exception: bool,
            **kwargs
    ):
        # TODO WIP - доделать универсальный вход: для вебхука и для ручного ввода
        if transaction.block_height < 0 or transaction.confirmations == 0:
            self.errors.append("transaction is not confirmed yet")

        if transaction_in_db := await BTCTransactionCRUD.find_one({
            "hash": transaction.hash,
        }):
            transaction_in_db = BTCTransactionInDB(**transaction_in_db)

        transaction.invoice_id = self.invoice.id

        if raise_exception and self.errors:
            raise HTTPException(HTTPStatus.BAD_REQUEST, self.errors)

        if transaction.confirmations < 3:
            await BTCTransactionCRUD.update_or_insert({"hash": transaction.hash}, transaction.dict())

        elif transaction.confirmations >= 3 and transaction_in_db.simba_tokens_issued:
            await BTCTransactionCRUD.update_one({"hash": transaction.hash}, transaction.dict())

        elif transaction.confirmations >= 3 and not transaction_in_db.simba_tokens_issued:
            await SimbaWrapper().validate_and_issue_tokens(
                self.invoice, incoming_btc=incoming_btc, comment=transaction.hash
            )
            transaction.simba_tokens_issued = True
            await BTCTransactionCRUD.update_one({"hash": transaction.hash}, transaction.dict())
            self.invoice.status = InvoiceStatus.COMPLETED
            self.invoice.btc_amount_proceeded += incoming_btc
            self.invoice.finised_at = datetime.now()

            await self.update_invoice()

        return True

    async def proceed_new_eth_transaction(self, transaction: EthereumTransaction, incoming_simba_tokens: int, **kwargs):
        pass

    async def proceed_new_transaction(
            self,
            transaction: Union[BTCTransaction, EthereumTransaction],
            *,
            raise_exception: bool = False,
            **kwargs
    ):
        if isinstance(transaction, BTCTransaction):
            return await self.proceed_new_btc_transaction(transaction, raise_exception, **kwargs)
        elif isinstance(transaction, EthereumTransaction):
            return await self.proceed_new_eth_transaction(transaction, raise_exception, **kwargs)
