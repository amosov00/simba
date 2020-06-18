from abc import ABC
from http import HTTPStatus
from typing import Union

from fastapi import HTTPException

from database.crud import BTCTransactionCRUD
from schemas import InvoiceInDB, InvoiceType, InvoiceStatus, BTCTransaction

__all__ = ["CryptoValidation", "ParseCryptoTransaction", "CryptoCurrencyRate"]


class CryptoCurrencyRate(ABC):
    # TODO Remove if not necessary

    # 1 BTC = 100,000,000 SATOSHI
    SATOSHI_IN_BTC = 10 ** 8
    # 1 BTC = 100,000,000 SIMBA
    SIMBA_IN_BTC = 10 ** 8

    @classmethod
    def btc_to_simba_tokens(cls, btc: int) -> int:
        return btc

    @classmethod
    def simba_tokens_to_btc(cls, simba_tokens: int) -> float:
        return simba_tokens / cls.SIMBA_IN_BTC


class ParseCryptoTransaction:
    @staticmethod
    def get_btc_amount_btc_transaction(transaction: BTCTransaction, btc_address: str):
        amount: int = 0
        objects = list(filter(lambda o: btc_address in o.addresses, transaction.outputs))

        for i in objects:
            amount += i.value

        return amount

    @staticmethod
    def get_simba_amount_eth_transaction():
        pass


class CryptoValidation(ABC):
    SIMBA_TOKENS_MINIMAL_AMOUNT = 200000

    # Делать независимую дполнительную логику для валидации исходящих данных

    def _validate_invoice(self, excepted_status: InvoiceStatus) -> bool:
        # TODO complete
        return True

    @classmethod
    async def validate_btc_transaction_with_invoice(cls, invoice: InvoiceInDB, transaction: BTCTransaction) -> bool:
        errors = []

        if invoice.status not in [InvoiceStatus.WAITING, InvoiceStatus.PROCESSING]:
            errors.append("Invalid invoice address")

        if not invoice.target_btc_address:
            errors.append("Invoice has no btc address")

        if await BTCTransactionCRUD.find_one({"hash": transaction.hash}):
            errors.append("Transaction already exists")

        if transaction.addresses:
            if invoice.target_btc_address not in transaction.addresses:
                errors.append("Target address is not found in transaction addresses")

        if transaction.inputs:
            target_address = list(
                filter(lambda o: invoice.target_btc_address in o.addresses, transaction.inputs)
            )

            if not target_address:
                errors.append("Target address is not found in transaction outputs")

        else:
            errors.append("Transaction has no outputs")
        # TODO uncomment later
        # if errors:
        #     raise HTTPException(HTTPStatus.BAD_REQUEST, errors)

        return True

    @classmethod
    def validate_simba_amount(cls, simba: int) -> bool:
        if simba and simba >= cls.SIMBA_TOKENS_MINIMAL_AMOUNT:
            return True

        return False

    @classmethod
    def validate_currency_rate(cls, btc: int, simba: int) -> bool:
        # TODO raise error if not valid
        status = simba / btc == 1
        return status
