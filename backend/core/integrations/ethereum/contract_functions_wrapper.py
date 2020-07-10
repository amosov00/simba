import asyncio
from http import HTTPStatus

from hexbytes import HexBytes
from web3 import Web3
from fastapi import HTTPException
from sentry_sdk import capture_message
import requests

from .base_wrapper import EthereumBaseContractWrapper
from schemas import EthereumContract
from config import GAS_STATION_ENDPOINT

GAS = 250000
GAS_PRICE = Web3.toWei("24", "gwei")

# Is necessary because of initial fee in 50k.
# If transaction is made with amount less than 50k, error will be raised
SIMBA_MIN_BASE_AMOUNT = 50000


class FunctionsContractWrapper(EthereumBaseContractWrapper):
    def __init__(self, contract: EthereumContract, admin_address: str, admin_private_key: str):
        super().__init__(contract)
        self.admin_address = Web3.toChecksumAddress(admin_address)
        self.admin_privkey = admin_private_key

    def _get_nonce(self):
        return self.w3.eth.getTransactionCount(self.admin_address)

    def _approve(self, amount: int, nonce: int) -> HexBytes:
        tx = self.contract.functions.approve(self.admin_address, amount).buildTransaction(
            {"gas": GAS, "gasPrice": GAS_PRICE, "from": self.admin_address, "nonce": nonce,}
        )
        signed_txn = self.w3.eth.account.signTransaction(tx, private_key=self.admin_privkey)
        return self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    def issue_coins(self, customer_address: str, amount: int, comment: str) -> HexBytes:
        """Simba contract"""
        if amount < SIMBA_MIN_BASE_AMOUNT:
            capture_message(f"trying to issue < 50k simba,\nETH ADDR: {customer_address}, BTC HASH {comment}")
            raise HTTPException(HTTPStatus.BAD_REQUEST, "minimal simba amount to issue - 50,000")

        customer_address = Web3.toChecksumAddress(customer_address)
        nonce = self._get_nonce()
        # TODO delete self._approve after success testing (after 8/07/2020)
        # self._approve(amount, nonce)

        try:
            gas_station_req = requests.get(GAS_STATION_ENDPOINT).json()
        except Exception:
            gas_station_req = None
        gas_station_gwei = str(int(gas_station_req.get("fast")) // 10) if gas_station_req and gas_station_req.get("fast") else "24"
        gas_price = Web3.toWei(gas_station_gwei, "gwei")
        tx = self.contract.functions.issue(customer_address, amount, comment).buildTransaction(
            {
                "gas": GAS,
                "gasPrice": gas_price if gas_price else GAS_PRICE,
                "from": self.admin_address,
                "nonce": nonce
            }
        )
        signed_txn = self.w3.eth.account.signTransaction(tx, private_key=self.admin_privkey)
        return self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    def redeem_coins(self):
        """Simba contract"""
        pass

    def freeze_and_transfer(self, customer_address: str, amount: int, period: int):
        """SST contract"""
        customer_address = Web3.toChecksumAddress(customer_address)
        nonce = self._get_nonce()
        tx = self.contract.functions.freezeAndTransfer(customer_address, amount, period).buildTransaction(
            {"gas": GAS, "gasPrice": GAS_PRICE, "from": self.admin_address, "nonce": nonce}
        )
        signed_txn = self.w3.eth.account.signTransaction(tx, private_key=self.admin_privkey)
        return self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
