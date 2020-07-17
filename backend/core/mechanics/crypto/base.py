from abc import ABC
from typing import Literal
from http import HTTPStatus

from fastapi import HTTPException

from schemas import InvoiceType, BTCTransaction
from config import SIMBA_BUY_SELL_FEE, SIMBA_MINIMAL_BUY_AMOUNT

__all__ = ["CryptoValidation", "ParseCryptoTransaction", "CryptoCurrencyRate"]


class CryptoCurrencyRate(ABC):
    # 1 BTC = 100,000,000 SATOSHI
    SATOSHI_IN_BTC = 10 ** 8
    # 1 BTC = 100,000,000 SIMBA
    SIMBA_IN_BTC = 10 ** 8

    SIMBA_IN_SST = 20000

    @classmethod
    def btc_to_simba_tokens(cls, btc: int) -> int:
        return btc

    @classmethod
    def simba_tokens_to_btc(cls, simba_tokens: int) -> float:
        return simba_tokens

    @classmethod
    def simba_to_sst(cls, simba_tokens: int) -> int:
        return round(simba_tokens / cls.SIMBA_IN_SST)


class ParseCryptoTransaction:
    @classmethod
    def get_output_by_btc_transaction(cls, transaction: BTCTransaction, btc_address: str):
        return list(filter(lambda o: btc_address in o.addresses, transaction.outputs))

    @classmethod
    def get_btc_amount_btc_transaction(cls, transaction: BTCTransaction, btc_address: str):
        amount: int = 0
        objects = cls.get_output_by_btc_transaction(transaction, btc_address)

        for i in objects:
            amount += i.value

        return amount

    @staticmethod
    def get_simba_amount_eth_transaction():
        pass


class CryptoValidation(ABC):
    @classmethod
    def validate_simba_amount(cls, simba: int) -> bool:
        return True if simba and simba >= SIMBA_MINIMAL_BUY_AMOUNT else False

    @classmethod
    def validate_currency_rate(
            cls,
            invoice_type: Literal[InvoiceType.SELL, InvoiceType.BUY],
            btc: int,
            simba: int
    ) -> bool:
        if not all([isinstance(btc, int), isinstance(simba, int)]):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "invalid btc or simba amount")
        if btc <= 0 or simba <= 0:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "invalid btc or simba amount")

        # TODO temp comment
        # if invoice_type == InvoiceType.BUY:
        #     if simba != btc:
        #         raise HTTPException(HTTPStatus.BAD_REQUEST, "invalid btc and simba ratio")

        # elif invoice_type == InvoiceType.SELL:
        #     if simba != btc + SIMBA_BUY_SELL_FEE:
        #         raise HTTPException(HTTPStatus.BAD_REQUEST, "invalid btc and simba ratio")
        # else:
        #     raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, "invalid invoice type")

        return True
