from abc import ABC
from typing import Union, List, Literal

import ujson
from ethereum_gasprice import (
    AsyncGaspriceController,
    AsyncEtherscanProvider,
    AsyncEthGasStationProvider,
    AsyncEtherchainProvider,
    AsyncPoaProvider,
    GaspriceStrategy,
    EthereumUnit
)
from hexbytes import HexBytes
from web3 import Web3
from web3.datastructures import AttributeDict

from config import ETH_MAX_GAS_PRICE_GWEI, TRANSACTION_MIN_CONFIRMATIONS, settings
from core.utils.decimal128 import to_decimal128
from schemas import EthereumContract

__all__ = ["EthereumBaseContractWrapper"]


class EthereumBaseWrapper(ABC):
    @classmethod
    async def get_actual_gasprice(cls):
        async with AsyncGaspriceController(
            return_unit=EthereumUnit.GWEI,
            providers=(AsyncEtherscanProvider, AsyncEthGasStationProvider, AsyncEtherchainProvider, AsyncPoaProvider),
            settings={
                AsyncEtherscanProvider.title: settings.crypto.etherscan_api_token,
                AsyncEthGasStationProvider.title: settings.crypto.gasstation_api_token,
            }
        ) as controller:
            gasprice = await controller.get_gasprice_by_strategy(GaspriceStrategy.FAST)

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

        for k, val in obj.items():
            if isinstance(val, HexBytes):
                obj[k] = val.hex().lower()
            elif isinstance(val, AttributeDict):
                obj[k] = cls.serialize(val)
            elif isinstance(val, str) and val.startswith("0x"):
                obj[k] = val.lower()
            elif isinstance(val, int) and val > 2147483647:
                # fix for OverflowError: MongoDB can only handle up to 8-byte ints
                obj[k] = to_decimal128(val)

        return obj


class EthereumBaseContractWrapper(EthereumBaseWrapper):
    def __init__(self, contract: EthereumContract):
        self.w3 = Web3(self.init_web3_provider("ws", settings.crypto.infura_ws_url))
        self.contract_meta = contract
        self.contract_address = Web3.toChecksumAddress(contract.address)

        if contract.abi_filepath:
            with open(contract.abi_filepath) as f:
                self.abi = ujson.load(f)

        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)

        self.transactions: List[dict] = []
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
