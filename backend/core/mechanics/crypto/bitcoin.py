from http import HTTPStatus
from typing import Optional, List, Tuple

from fastapi import HTTPException
from pycoin.coins.tx_utils import create_signed_tx
from sentry_sdk import capture_message

from config import BTC_FEE, settings
from core.integrations.blockcypher import BlockCypherAPIWrapper
from core.integrations.pycoin_wrapper import PycoinWrapper
from database.crud import BTCAddressCRUD
from schemas import User, InvoiceInDB, BTCTransaction, BTCAddress, ObjectIdPydantic
from .base import CryptoValidation, ParseCryptoTransaction


class BitcoinWrapper(CryptoValidation, ParseCryptoTransaction):
    def __init__(self):
        self.api_wrapper = BlockCypherAPIWrapper()
        self.hot_wallet_balance = 0
        self.multisig_wallet_balance = 0

    @staticmethod
    def _validate_payables(payables: List[Tuple[str, int]]) -> bool:
        # TODO дописать валидацию
        for payable in payables:
            if payable[1] == 0:
                capture_message("Invalid payable amount")
                raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, "Invalid payable")

        return True

    @classmethod
    async def create_wallet_address(cls, invoice: InvoiceInDB, user: User):
        inst = await PycoinWrapper(user=user, invoice=invoice).from_active_xpub()
        return await inst.generate_new_address()

    async def fetch_transaction(self, transaction_hash: str) -> BTCTransaction:
        return await self.api_wrapper.fetch_transaction_info(transaction_hash)

    async def fetch_address_and_save(
            self,
            address: str,
            *,
            invoice_id: ObjectIdPydantic = None,
            user_id: ObjectIdPydantic = None,
            save: bool = True
    ) -> Optional[BTCAddress]:
        address_info = await self.api_wrapper.fetch_address_info(address) if address else None
        if address_info:
            address_info.user_id = user_id
            address_info.invoice_id = invoice_id

        if address_info and save:
            await BTCAddressCRUD.update_or_create(
                address_info.address, address_info.dict(exclude_defaults=True, exclude_unset=True)
            )

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
        btc_difference = self.hot_wallet_balance - amount - fee
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
        fee = fee or BTC_FEE
        self.hot_wallet_balance = await self.api_wrapper.current_balance(
            settings.crypto.btc_hot_wallet_address
        )
        spendables = await self.api_wrapper.get_spendables(settings.crypto.btc_hot_wallet_address)
        payables = self.proceed_payables(address, amount, settings.crypto.btc_hot_wallet_address, fee)

        self._validate_payables(payables)

        if not spendables:
            capture_message("Invalid spendables value", level="error")
            raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, "Invalid spendables value")

        tx = create_signed_tx(
            self.api_wrapper.network,
            spendables=spendables,
            payables=payables,
            wifs=[settings.crypto.btc_hot_wallet_wif, ],
            fee=fee,
        )
        return await self.api_wrapper.push_raw_tx(tx)

