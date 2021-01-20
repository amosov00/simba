from abc import ABC
from decimal import Decimal
from sys import getsizeof
from typing import Union, List, Literal

import ujson
from bson import Decimal128
from hexbytes import HexBytes
from web3 import Web3
from web3.datastructures import AttributeDict

from config import ETH_MAX_GAS_PRICE_GWEI, TRANSACTION_MIN_CONFIRMATIONS, settings
from core.utils import gasprice_from_etherscan, gasprice_from_ethgasstation
from schemas import EthereumContract, EthereumTransaction

__all__ = ["EthereumBaseCommonWrapper", "EthereumBaseContractWrapper"]


class EthereumBaseWrapper(ABC):
    gasprice_wrapper = gasprice_from_etherscan

    @classmethod
    async def get_actual_gasprice(cls):
        gasprice = await cls.gasprice_wrapper()

        if not gasprice:
            gasprice = await gasprice_from_ethgasstation()

        return Web3.toWei(min(int(gasprice), ETH_MAX_GAS_PRICE_GWEI), "gwei")

    @classmethod
    def init_web3_provider(cls, provider_type: Literal["http", "ws"], provider_url: str, websocket_timeout: int = 60):
        if provider_type == "http":
            return Web3.HTTPProvider(provider_url)
        elif provider_type == "ws":
            return Web3.WebsocketProvider(provider_url, websocket_timeout=websocket_timeout)
        else:
            raise ValueError("Invalid provider type")

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
            try:
                obj = Decimal128(Decimal(obj))
            except Exception:
                # TODO bypass error with big int (decimal.Inexact: [<class 'decimal.Inexact'>])
                obj = str(obj)

        return obj


class EthereumBaseCommonWrapper(EthereumBaseWrapper):
    def __init__(self):
        self.w3 = Web3(self.init_web3_provider("ws", settings.crypto.infura_ws_url))
        self.blocks: List[EthereumTransaction] = []


class EthereumBaseContractWrapper(EthereumBaseWrapper):
    def __init__(self, contract: EthereumContract):
        pass
        # Temp fix cause of Infura maintenance
        self.w3 = Web3(self.init_web3_provider("ws", contract.provider_ws_link))
        # self.w3 = Web3(self.init_web3_provider("http", contract.provider_http_link))
        self.contract_meta = contract
        self.contract_address = Web3.toChecksumAddress(contract.address)

        if contract.abi_filepath:
            with open(contract.abi_filepath) as f:
                self.abi = ujson.load(f)

        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)

        self.blocks: List[EthereumTransaction] = []
        self.filters = []
        self._last_block = None
        self._contract_events = []
        self.min_confirmations = TRANSACTION_MIN_CONFIRMATIONS

    def fetch_transaction_by_hash(self, transaction_hash: Union[str, HexBytes]):
        return self.w3.eth.getBlock(transaction_hash, full_transactions=True)

    @property
    def last_block(self):
        if not self._last_block:
            self._last_block = self.contract.web3.eth.blockNumber
        return self._last_block

    @property
    def contract_events(self):
        if not self._contract_events:
            self._contract_events = self._get_contract_events_titles()
        return self._contract_events

    def _get_contract_events_titles(self) -> list:
        events = []
        for key, _ in self.contract.events.__dict__.items():
            if key != "abi" and not key[0].startswith("_"):
                events.append(key)

        return events

    def _get_contract_event_by_title(self, contract_title: str):
        return self.contract.events[contract_title]
