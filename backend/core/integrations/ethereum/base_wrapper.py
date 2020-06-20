from abc import ABC
from typing import Union

from sys import getsizeof
from decimal import Decimal

import ujson
from hexbytes import HexBytes
from bson import Decimal128
from web3 import Web3
from web3.datastructures import AttributeDict

from schemas import EthereumContract
from config import INFURA_WS_URL


class EthereumBaseWrapper(ABC):
    def __init__(self, contract: EthereumContract):
        _abi = []
        _bin = None
        self.w3 = Web3(Web3.WebsocketProvider(contract.provider_ws_link, websocket_timeout=60))
        self.contract_meta = contract
        self.contract_address = Web3.toChecksumAddress(contract.address)

        if contract.abi_filepath:
            with open(contract.abi_filepath) as f:
                self.abi = ujson.load(f)

        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)

        self.contract_events = []
        self.blocks = []
        self.filters = []
        self.last_block = None

    @classmethod
    def serialize(cls, obj) -> dict:
        if isinstance(obj, AttributeDict):
            obj = dict(obj)
            for key, val in obj.items():
                obj[key] = cls.serialize(val)

        elif isinstance(obj, HexBytes):
            obj = obj.hex()

        elif isinstance(obj, int) and getsizeof(obj) >= 32:
            # fix for OverflowError: MongoDB can only handle up to 8-byte ints
            obj = Decimal128(Decimal(obj))

        return obj

    def fetch_transaction_by_hash(self, transaction_hash: Union[str, HexBytes]):
        # if isinstance(transaction_hash, str):
        #     transaction_hash = Web3.toHex(transaction_hash)
        return self.w3.eth.getBlock(
            transaction_hash,
            full_transactions=True
        )
