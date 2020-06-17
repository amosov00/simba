from abc import ABC
from typing import Union

from pydantic import ValidationError

from schemas import InvoiceInDB, InvoiceType, InvoiceStatus


class CryptoCurrencyRate(ABC):
    # TODO Remove if not necessary

    # 1 BTC = 100,000,000 SATOSHI
    SATOSHI_IN_BTC = 10 ** 8
    # 1 BTC = 100,000,000 SIMBA
    SIMBA_IN_BTC = 10 ** 8

    @classmethod
    def btc_to_simba_tokens(cls, btc: int) -> int:
        return round(btc * cls.SIMBA_IN_BTC)

    @classmethod
    def simba_tokens_to_btc(cls, simba_tokens: int) -> float:
        return simba_tokens / cls.SIMBA_IN_BTC


class CryptoValidation(ABC):
    SIMBA_TOKENS_MINIMAL_AMOUNT = 200000
    # Делать независимую дполнительную логику для валидации исходящих данных

    def _validate_invoice(self, excepted_status: InvoiceStatus) -> bool:
        invoice: InvoiceInDB = getattr(self, "invoice", None)

        if not invoice:
            raise AttributeError("Invoice is not found")

        if not invoice.status == excepted_status:
            raise AttributeError("Invalid invoice status")

        if invoice.invoice_type == InvoiceType.BUY:
            for field in ("user_id", "btc_tx", "btc_amount_deposited"):
                if not getattr(invoice, field, False):
                    raise AttributeError(f"'{field}' field from invoice is missing")

        elif invoice.invoice_type == InvoiceType.SELL:
            # TODO fill it
            pass

        if not self._validate_currency_rate(invoice.btc_amount, invoice.simba_amount):
            raise AttributeError(f"Invalid cryptocurrencies rates")

        return True

    def _validate_fee(self):
        pass

    @classmethod
    def validate_simba_amount(cls, simba: int) -> bool:
        if simba and simba >= cls.SIMBA_TOKENS_MINIMAL_AMOUNT:
            return True

        return False

    @classmethod
    def validate_currency_rate(cls, btc: int, simba: int) -> bool:
        status = simba / btc == 1
        # TODO raise error if not valid
        return status
