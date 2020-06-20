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

    async def proceed_new_btc_transaction(self, transaction: BTCTransaction, incoming_btc: int, **kwargs):
        pass

    async def proceed_new_eth_transaction(self, transaction: EthereumTransaction, incoming_simba_tokens: int, **kwargs):
        pass

    async def proceed_new_transaction(self, transaction: Union[BTCTransaction, EthereumTransaction], **kwargs):
        if isinstance(transaction, BTCTransaction):
            return await self.proceed_new_btc_transaction(transaction, **kwargs)
        elif isinstance(transaction, EthereumTransaction):
            return await self.proceed_new_eth_transaction(transaction, **kwargs)
