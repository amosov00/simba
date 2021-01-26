from http import HTTPStatus

from fastapi import HTTPException
from hexbytes import HexBytes
from sentry_sdk import capture_message
from web3 import Web3

from config import SIMBA_BUY_SELL_FEE, ETH_MAX_GAS
from schemas import EthereumContract
from .base_wrapper import EthereumBaseContractWrapper


class FunctionsContractWrapper(EthereumBaseContractWrapper):
    def __init__(self, contract: EthereumContract, admin_address: str, admin_private_key: str):
        super().__init__(contract)
        self.admin_address = Web3.toChecksumAddress(admin_address)
        self.admin_privkey = admin_private_key
        self.simba_fee = SIMBA_BUY_SELL_FEE

    def _get_nonce(self):
        return self.w3.eth.getTransactionCount(self.admin_address, "pending")

    def check_min_amount(self, amount: int, *, func_name: str = None, comment: str = None) -> bool:
        if amount < self.simba_fee:
            capture_message(
                f"trying to {func_name or 'call some contranc func'} < {self.simba_fee} simba, BTC HASH {comment or '?'}"
            )
            raise HTTPException(HTTPStatus.BAD_REQUEST, f"minimal simba amount to issue - {self.simba_fee}")

        return True

    async def issue_coins(self, customer_address: str, amount: int, comment: str) -> HexBytes:
        """Simba contract."""
        self.check_min_amount(amount, func_name="issue", comment=comment)

        customer_address = Web3.toChecksumAddress(customer_address)

        tx = self.contract.functions.issue(customer_address, amount, comment).buildTransaction(
            {
                "gas": ETH_MAX_GAS,
                "gasPrice": await self.get_actual_gasprice(),
                "from": self.admin_address,
                "nonce": self._get_nonce(),
            }
        )
        signed_txn = self.w3.eth.account.signTransaction(tx, private_key=self.admin_privkey)
        return self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    async def redeem_coins(self, amount: int, comment: str):
        """Simba contract."""
        self.check_min_amount(amount, func_name="redeem", comment=comment)

        tx = self.contract.functions.redeem(amount, comment).buildTransaction(
            {
                "gas": ETH_MAX_GAS,
                "gasPrice": await self.get_actual_gasprice(),
                "from": self.admin_address,
                "nonce": self._get_nonce(),
            }
        )
        signed_txn = self.w3.eth.account.signTransaction(tx, private_key=self.admin_privkey)
        return self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    async def freeze_and_transfer(self, customer_address: str, amount: int, period: int):
        """SST contract."""
        customer_address = Web3.toChecksumAddress(customer_address)
        tx = self.contract.functions.freezeAndTransfer(customer_address, amount, period).buildTransaction(
            {
                "gas": ETH_MAX_GAS,
                "gasPrice": await self.get_actual_gasprice(),
                "from": self.admin_address,
                "nonce": self._get_nonce(),
            }
        )
        signed_txn = self.w3.eth.account.signTransaction(tx, private_key=self.admin_privkey)
        return self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    async def balance_of(self, address: str):
        address = Web3.toChecksumAddress(address)
        return self.contract.functions.balanceOf(address).call()
