import logging
from http import HTTPStatus
from typing import Union, Optional, List

from fastapi import HTTPException

from database.crud import InvoiceCRUD
from schemas import (
    User,
    InvoiceInDB,
    InvoiceExtended,
    BTCTransactionOutputs,
    EthereumTransactionInDB,
    EthereumTransaction,
    SimbaContractEvents,
)


class InvoiceBase:
    def __init__(self, invoice: Union[dict, InvoiceInDB, InvoiceExtended], user: Union[dict, User] = None):
        if isinstance(invoice, dict):
            invoice = InvoiceInDB(**invoice)

        if user and isinstance(user, dict):
            user = User(**user)

        self.invoice = invoice
        self.user = user
        self.errors = []

        assert invoice.id, "invoice id is missing"

    def _log(self, msg: str, level: str = "info"):
        # TODO refactor later
        log_map = {"info": 20, "warning": 30, "error": 40}
        return logging.log(log_map.get(level, 20), f"Invoice {self.invoice.id}: {msg}")

    def _raise_exception_if_exists(self):
        if self.errors:
            raise HTTPException(HTTPStatus.BAD_REQUEST, self.errors)
        else:
            return None

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

        if transaction.event in SimbaContractEvents.ALL:
            value = transaction.args.get("value")

        return value

    async def update_invoice(self):
        return await InvoiceCRUD.update_one({"_id": self.invoice.id}, self.invoice.dict(exclude={"id"}))
