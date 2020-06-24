import asyncio

from hexbytes import HexBytes
from bson import Decimal128
from web3 import Web3
from web3.contract import prepare_transaction, build_transaction_for_function
from web3.datastructures import AttributeDict

from .base_wrapper import EthereumBaseWrapper
from schemas import EthereumContract

GAS = 250000
GAS_PRICE = Web3.toWei("1", "gwei")
GAS_LIMIT = 50000


class ContractFunctionsWrapper(EthereumBaseWrapper):
    def __init__(self, contract: EthereumContract, admin_address: str, admin_private_key: str):
        super().__init__(contract)
        self.admin_address = Web3.toChecksumAddress(admin_address)
        self.admin_privkey = admin_private_key

    def _get_nonce(self):
        return Web3.toHex(self.w3.eth.getTransactionCount(self.admin_address, "pending"))

    def _approve(self, amount: int) -> HexBytes:
        tx = self.contract.functions.approve(
            self.admin_address, amount
        ).buildTransaction({
            'gas': GAS,
            'gasPrice': GAS_PRICE,
            'from': self.admin_address,
            'nonce': self._get_nonce(),
        })
        signed_txn = self.w3.eth.account.signTransaction(tx, private_key=self.admin_privkey)
        return self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    def issue_coins(self, customer_address: str, amount: int, comment: str) -> HexBytes:
        """Simba contract"""
        customer_address = Web3.toChecksumAddress(customer_address)
        self._approve(amount)
        tx = self.contract.functions.issue(
            customer_address, amount, comment
        ).buildTransaction({
            'gas': GAS,
            'gasPrice': GAS_PRICE,
            'from': self.admin_address,
            'nonce': self._get_nonce(),
        })
        signed_txn = self.w3.eth.account.signTransaction(tx, private_key=self.admin_privkey)
        return self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    def freeze_and_transfer(self, customer_address: str, amount: int, period: int):
        """SST contract"""
        customer_address = Web3.toChecksumAddress(customer_address)
        tx = self.contract.functions.freezeAndTransfer(
            customer_address, amount, period
        ).buildTransaction({
            'gas': GAS,
            'gasPrice': GAS_PRICE,
            'from': self.admin_address,
            'nonce': self._get_nonce(),
        })
        signed_txn = self.w3.eth.account.signTransaction(tx, private_key=self.admin_privkey)
        return self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
