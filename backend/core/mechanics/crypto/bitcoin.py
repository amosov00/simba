from typing import Union, Optional, List, Tuple
from http import HTTPStatus

from pycoin.coins.tx_utils import create_signed_tx
from sentry_sdk import capture_message
from fastapi import HTTPException

from core.integrations.blockcypher import BlockCypherAPIWrapper
from core.integrations.pycoin_wrapper import PycoinWrapper
from database.crud import UserCRUD, BTCAddressCRUD, BTCTransactionCRUD, InvoiceCRUD
from schemas import User, InvoiceInDB, InvoiceStatus, BTCTransaction, BTCAddress, ObjectIdPydantic
from .base import CryptoValidation, ParseCryptoTransaction
from config import BTC_HOT_WALLET_ADDRESS, BTC_HOT_WALLET_WIF, BTC_COLD_WALLET_XPUB


class BitcoinWrapper(CryptoValidation, ParseCryptoTransaction):
    FEE = 10000
    BTC_HOT_WALLET_WIF = BTC_HOT_WALLET_WIF
    BTC_HOT_WALLET_ADDRESS = BTC_HOT_WALLET_ADDRESS

    def __init__(self):
        self.api_wrapper = BlockCypherAPIWrapper()
        self.service_wallet_balance = 0

    @staticmethod
    def _validate_payables(payables: List[Tuple[str, int]]) -> bool:
        # TODO дописать валидацию
        for payable in payables:
            if payable[1] == 0:
                capture_message("Invalid payable amount")
                raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, "Invalid payable")

        return True

    async def fetch_address_and_save(
            self,
            address: str,
            *,
            invoice_id: ObjectIdPydantic = None,
            user_id: ObjectIdPydantic = None,
            save: bool = True
    ) -> Optional[BTCAddress]:
        address_info = await self.api_wrapper.fetch_address_info(address)
        if address_info:
            address_info.user_id = user_id
            address_info.invoice_id = invoice_id

        if address_info and save:
            await BTCAddressCRUD.update_or_create(address_info.address, address_info.dict())

        return address_info

    def proceed_payables(
            self, destination_address: str, amount: int, address_from: str, fee: Optional[int] = None
    ) -> List[Tuple[str, int]]:
        """
        Струкрура payable (address, satoshi)
        destination_payables - Payable клиентского кошелька
        difference_payables - Разница, которую нужно отправить на сервисный кошелек
        address from - адрес отправляющего кошелька
        :return:
        """
        btc_difference = self.service_wallet_balance - amount - fee
        destination_payable = (destination_address, amount)
        difference_payable = (address_from, btc_difference)

        return [destination_payable, difference_payable]

    async def create_and_sign_transaction(
            self, address: str, amount: int, fee: Optional[int] = None,
    ) -> BTCTransaction:
        """
        Payables передавать в форме [(<address_hash>, <btc_amount>), ], btc_amount - in satoshi
        destination_payables - Payable клиентского кошелька
        Wif передавать в формате [<wif>, ]
        """
        fee = fee or self.FEE
        self.service_wallet_balance = await self.api_wrapper.current_balance(self.BTC_HOT_WALLET_ADDRESS)
        spendables = await self.api_wrapper.get_spendables(self.BTC_HOT_WALLET_ADDRESS)
        payables = self.proceed_payables(address, amount, self.BTC_HOT_WALLET_ADDRESS, fee)

        self._validate_payables(payables)

        tx = create_signed_tx(
            self.api_wrapper.network,
            spendables=spendables,
            payables=payables,
            wifs=[self.BTC_HOT_WALLET_WIF, ],
            fee=fee,
        )
        result = await self.api_wrapper.push_raw_tx(tx)
        result = result.get("tx")
        return BTCTransaction(**result) if result else None

    async def _create_wallet_address(self, invoice: dict):
        """ TODO Deprecated, delete after 15/07/20 """
        resp = await self.api_wrapper.create_wallet_address(1)

        if "errors" in resp:
            capture_message("error while creating wallet")
            raise HTTPException(HTTPStatus.BAD_REQUEST, "error while creating wallet")

        address = resp["chains"][0]["chain_addresses"][0]
        address_full_info = await self.api_wrapper.fetch_address_info(address.get("address"))
        address_full_info.invoice_id = invoice["_id"]
        address_full_info.public_key = address.get("public")
        address_full_info.path = address.get("path")

        await BTCAddressCRUD.insert_one(address_full_info.dict())
        await InvoiceCRUD.update_one({"_id": invoice["_id"]}, {"target_btc_address": address_full_info.address})

        return address_full_info.address

    async def create_wallet_address(self, invoice: dict, user: User):
        invoice = InvoiceInDB(**invoice)
        created_address = await PycoinWrapper(BTC_COLD_WALLET_XPUB, user=user, invoice=invoice).generate_new_address()
        await self.fetch_address_and_save(created_address, invoice_id=invoice.id, user_id=user.id)
        await InvoiceCRUD.update_one({"_id": invoice.id}, {"target_btc_address": created_address})
        return created_address

    async def fetch_transaction(self, invoice: InvoiceInDB, transaction_hash: str) -> BTCTransaction:
        return await self.api_wrapper.fetch_transaction_info(transaction_hash)

    async def fetch_and_save_transaction(self, invoice: InvoiceInDB, transaction_hash: str) -> dict:
        """
        TODO deprecated
        """
        transaction = await self.api_wrapper.fetch_transaction_info(transaction_hash)

        await self.validate_btc_transaction_with_invoice(invoice, transaction)

        tx_id = (await BTCTransactionCRUD.insert_one(transaction.dict())).inserted_id

        incoming_btc = self.get_btc_amount_btc_transaction(transaction, invoice.target_btc_address)

        invoice.btc_tx_ids = list({*invoice.btc_tx_ids, tx_id})
        invoice.status = InvoiceStatus.COMPLETED
        invoice.btc_amount_proceeded = (
            invoice.btc_amount_proceeded + incoming_btc if invoice.btc_amount_proceeded else incoming_btc
        )

        await InvoiceCRUD.update_one({"_id": invoice.id}, invoice.dict(exclude={"_id"}))

        return {"incoming_btc": incoming_btc, "tx_hash": transaction.hash}
