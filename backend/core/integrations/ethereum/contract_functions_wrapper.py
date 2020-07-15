import asyncio
from http import HTTPStatus
import logging

from hexbytes import HexBytes
from web3 import Web3
from fastapi import HTTPException
from sentry_sdk import capture_message

from .base_wrapper import EthereumBaseContractWrapper
from core.utils import gas_price_from_ethgasstation
from schemas import EthereumContract

GAS = 250000

# Is necessary because of initial fee in 50k.
# If transaction is made with amount less than 50k, error will be raised
SIMBA_BUY_SELL_FEE = 50000


class FunctionsContractWrapper(EthereumBaseContractWrapper):
    def __init__(self, contract: EthereumContract, admin_address: str, admin_private_key: str):
        super().__init__(contract)
        self.admin_address = Web3.toChecksumAddress(admin_address)
        self.admin_privkey = admin_private_key
        self.simba_fee = SIMBA_BUY_SELL_FEE

    def _get_nonce(self):
        return self.w3.eth.getTransactionCount(self.admin_address, "pending")

    @staticmethod
    async def get_gas_price():
        actual_gas_price_gwei = await gas_price_from_ethgasstation()
        return Web3.toWei(actual_gas_price_gwei, "gwei")

    def check_min_amount(self, amount: int, *, func_name: str = None, comment: str = None) -> bool:
        if amount < self.simba_fee:
            capture_message(
                f"trying to {func_name or 'call some contranc func'} < 50k simba, BTC HASH {comment or '?'}"
            )
            raise HTTPException(HTTPStatus.BAD_REQUEST, "minimal simba amount to issue - 50,000")

        return True

    async def issue_coins(self, customer_address: str, amount: int, comment: str) -> HexBytes:
        """Simba contract"""
        self.check_min_amount(amount, func_name="issue", comment=comment)

        customer_address = Web3.toChecksumAddress(customer_address)

        tx = self.contract.functions.issue(customer_address, amount, comment).buildTransaction(
            {
                "gas": GAS,
                "gasPrice": await self.get_gas_price(),
                "from": self.admin_address,
                "nonce": self._get_nonce()
            }
        )
        signed_txn = self.w3.eth.account.signTransaction(tx, private_key=self.admin_privkey)
        return self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    async def redeem_coins(self, amount: int, comment: str):
        """Simba contract"""
        self.check_min_amount(amount, func_name="redeem", comment=comment)

        tx = self.contract.functions.redeem(amount, comment).buildTransaction(
            {
                "gas": GAS,
                "gasPrice": await self.get_gas_price(),
                "from": self.admin_address,
                "nonce": self._get_nonce()
            }
        )
        signed_txn = self.w3.eth.account.signTransaction(tx, private_key=self.admin_privkey)
        return self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    async def freeze_and_transfer(self, customer_address: str, amount: int, period: int):
        """SST contract"""
        customer_address = Web3.toChecksumAddress(customer_address)
        tx = self.contract.functions.freezeAndTransfer(customer_address, amount, period).buildTransaction(
            {
                "gas": GAS,
                "gasPrice": await self.get_gas_price(),
                "from": self.admin_address,
                "nonce": self._get_nonce()
            }
        )
        signed_txn = self.w3.eth.account.signTransaction(tx, private_key=self.admin_privkey)
        return self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
