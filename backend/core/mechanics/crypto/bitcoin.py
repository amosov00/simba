from typing import Union, Optional, List, Tuple

from pycoin.coins.tx_utils import create_signed_tx

from core.integrations.blockcypher import BlockCypherAPIWrapper
from database.crud import UserCRUD, BTCAddressCRUD, BTCTransactionCRUD, InvoiceCRUD
from schemas import User, InvoiceInDB, InvoiceStatus
from .base import CryptoValidation, ParseCryptoTransaction


class BitcoinWrapper(CryptoValidation, ParseCryptoTransaction):
    FEE = 15000

    def __init__(self):
        self.api_wrapper = BlockCypherAPIWrapper()
        self.service_wallet_balance = 0

    @staticmethod
    def _validate_payables(payables: List[Tuple[str, int]]) -> bool:
        return True

    async def proceed_payables(
            self,
            destination_payables: Tuple[str, int],
            address_from: str
    ) -> List[Tuple[str, int]]:
        """
        Струкрура payable (address, satoshi)
        destination_payables - Payable клиентского кошелька
        difference_payables - Разница, которую нужно отправить на сервисный кошелек
        :return:
        """
        btc_outcome = self.service_wallet_balance - destination_payables[1] - self.FEE

        difference_payables = (address_from, btc_outcome)

        return [
            destination_payables,
            difference_payables
        ]

    async def create_and_sign_transaction(
            self,
            destination_payables: Tuple[str, int],
            address_from: str,
            wifs: List[str],
            fee: Union[int, str] = "standard",
    ):
        """
        Payables передавать в форме [(<address_hash>, <btc_amount>), ]
        destination_payables - Payable клиентского кошелька
        Wif передавать в формате [<wif>, ]
        """
        self.service_wallet_balance = await self.api_wrapper.current_balance(address_from)
        spendables = await self.api_wrapper.get_spendables(address_from)
        payables = await self.proceed_payables(destination_payables, address_from)

        self._validate_payables(payables)

        tx = create_signed_tx(
            self.api_wrapper.network,
            spendables=spendables,
            payables=payables,
            wifs=wifs,
            fee=self.FEE,
        )
        return await self.api_wrapper.push_raw_tx(tx)

    async def create_wallet_address(self, user: User):
        resp = await self.api_wrapper.create_wallet_address(1)
        if "errors" in resp:
            pass

        address = resp["chains"][0]["chain_addresses"][0]
        address_full_info = await self.api_wrapper.fetch_address_info(
            address.get("address")
        )
        address_full_info.user_id = user.id
        address_full_info.public_key = address.get("public")
        address_full_info.path = address.get("path")

        await BTCAddressCRUD.insert_one(address_full_info.dict())
        await UserCRUD.update_one({"_id": user.id}, {"btc_address": address_full_info.address})

        return address_full_info.address

    async def fetch_and_save_transaction(self, invoice: InvoiceInDB, transaction_hash: str) -> dict:
        """

        """
        transaction = await self.api_wrapper.fetch_transaction_info(transaction_hash)

        await self.validate_btc_transaction_with_invoice(invoice, transaction)

        tx_id = (
            await BTCTransactionCRUD.insert_one(transaction.dict())
        ).inserted_id

        incoming_btc = self.get_btc_amount_btc_transaction(transaction, invoice.target_btc_address)

        invoice.btc_tx_ids = list({*invoice.btc_tx_ids, tx_id})
        invoice.status = InvoiceStatus.COMPLETED
        invoice.btc_amount_proceeded = invoice.btc_amount_proceeded + incoming_btc \
            if invoice.btc_amount_proceeded else incoming_btc

        await InvoiceCRUD.update_one(
            {"_id": invoice.id},
            invoice.dict(exclude={"_id"})
        )

        return {
            "incoming_btc": incoming_btc,
            "tx_hash": transaction.hash
        }
