from typing import Union
from http import HTTPStatus

from fastapi import HTTPException

from .crypto.base import CryptoValidation
from schemas import InvoiceInDB, InvoiceType, BTCTransaction, EthereumTransaction


class InvoiceMechanics(CryptoValidation):
    def __init__(self, invoice: Union[dict, InvoiceInDB]):
        if isinstance(invoice, dict):
            invoice = InvoiceInDB(**invoice)

        self.invoice = invoice
        self.errors = []

    def _validate_common(self):
        if not getattr(self.invoice, "user_id", None):
            self.errors.append("`user_id` field is missing")

        return None

    def _validate_for_buy(self):
        if not self.validate_currency_rate(self.invoice.btc_amount, self.invoice.simba_amount):
            self.errors.append("invalid rate")

        if not self.validate_simba_amount(self.invoice.simba_amount):
            self.errors.append(f"min simba token amount: {self.SIMBA_TOKENS_MINIMAL_AMOUNT}")

        # TODO other fields
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

    async def proceed_btc_transaction(self, transaction: BTCTransaction):
        pass

    async def proceed_eth_transaction(self, transaction: EthereumTransaction):
        pass

    async def proceed_new_transaction(self, transaction: Union[BTCTransaction, EthereumTransaction]):
        if isinstance(transaction, BTCTransaction):
            return await self.proceed_btc_transaction(transaction)
        elif isinstance(transaction, EthereumTransaction):
            return await self.proceed_eth_transaction(transaction)
