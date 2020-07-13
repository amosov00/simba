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
    # Класс для валидации количества значений криптовалют
    # TODO синхронизировать с InvoiceMechanics().validate(). Есть повторяющиеся элементы
    SIMBA_TOKENS_MINIMAL_AMOUNT = 200000
    SIMBA_BUY_SELL_FEE = 50000

    @classmethod
    async def validate_btc_transaction_with_invoice(
            cls, invoice: InvoiceInDB, transaction: BTCTransaction
    ) -> bool:
        """ TODO deprecated ? """
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

        if errors:
            raise HTTPException(HTTPStatus.BAD_REQUEST, errors)

        return True

    @classmethod
    def validate_simba_amount(cls, simba: int) -> bool:
        if simba and simba >= cls.SIMBA_TOKENS_MINIMAL_AMOUNT:
            return True

        return False

    @classmethod
    def validate_currency_rate(cls, btc: int, simba: int) -> bool:
        if not all([isinstance(btc, int), isinstance(simba, int)]):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "invalid btc or simba amount")
        if btc <= 0 or simba <= 0:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "invalid btc or simba amount")
        if simba / btc != 1:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "invalid btc or simba ratio")

        return True
