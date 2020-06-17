from abc import ABC
from typing import Union

from pydantic import ValidationError

from schemas import InvoiceInDB, InvoiceType, InvoiceStatus


class CryptoCurrencyRate(ABC):
    # 1 BTC = 100,000,000 SIMBA
    SIMBA_IN_BTC = 10 ** 8

    @classmethod
    def btc_to_simba_tokens(cls, btc: int) -> int:
        return round(btc * cls.SIMBA_IN_BTC)

    @classmethod
    def simba_tokens_to_btc(cls, simba_tokens: int) -> float:
        return simba_tokens / cls.SIMBA_IN_BTC


class CryptoValidation(ABC):
    # Делать независимую логику для валидации исходящих данных

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

    def _validate_amount(self):
        pass

    @staticmethod
    def _validate_currency_rate(btc: Union[int, float], simba: Union[int, float]) -> bool:
        status = simba / btc == 100000000
        # TODO raise error if not valid
        return status
