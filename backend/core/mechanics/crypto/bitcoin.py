from typing import Union, Optional, List, Tuple

from pycoin.coins.tx_utils import create_signed_tx

from core.integrations.blockcypher import BlockCypherAPIWrapper
from database.crud import UserCRUD, BTCAddressCRUD, BTCTransactionCRUD, InvoiceCRUD
from schemas import User, InvoiceInDB, InvoiceStatus
from .base import CryptoValidation, ParseCryptoTransaction


class BitcoinWrapper(CryptoValidation, ParseCryptoTransaction):
    def __init__(self):
        self.api_wrapper = BlockCypherAPIWrapper()

    async def create_and_sign_transaction(
            self,
            spendables: List[Tuple[str, int]],
            address_from: str,
            wifs: List[str],
            fee: Union[int, str] = "standard",
    ):
        """
        Spendables передавать в форме [(<address_hash>, <btc_amount>), ]
        Wif передавать в формате [<wif>, ]
        """
        payables = await self.api_wrapper.get_payables(address_from)

        tx = create_signed_tx(
            self.api_wrapper.network,
            spendables=spendables,
            payables=payables,
            wifs=wifs,
            fee=fee
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

        invoice.btc_tx = list({*invoice.btc_tx, tx_id})
        invoice.btc_amount_deposited = invoice.btc_amount_deposited + incoming_btc \
            if invoice.btc_amount_deposited else incoming_btc

        await InvoiceCRUD.update_one(
            {"_id": invoice.id},
            {
                "btc_tx": invoice.btc_tx,
                "status": InvoiceStatus.COMPLETED,
                "btc_amount_deposited": invoice.btc_amount_deposited,
            }
        )

        return {
            "incoming_btc": incoming_btc,
            "tx_hash": transaction.hash
        }
