import asyncio
from os import path
from sys import getsizeof
import logging
from typing import Optional, Union
from decimal import Decimal
from websockets import ConnectionClosedError

import ujson
from hexbytes import HexBytes
from bson import Decimal128
from web3 import Web3
from web3.datastructures import AttributeDict
from web3.contract import ContractEvent, LogFilter
from sentry_sdk import capture_exception

from schemas import EthereumContract
from config import BASE_DIR, INFURA_WS_URL
from database.crud import EthereumTransactionCRUD

__all__ = ["EthereumContractWrapper"]


class EthereumContractWrapper:
    def __init__(self, contract: EthereumContract):
        _abi = []
        _bin = None
        self.w3 = Web3(Web3.WebsocketProvider(INFURA_WS_URL, websocket_timeout=60))
        self.contract_meta = contract
        self.contract_address = Web3.toChecksumAddress(contract.address)

        if contract.abi_filepath:
            with open(contract.abi_filepath) as f:
                _abi = ujson.load(f)

        self.contract = self.w3.eth.contract(address=self.contract_address, abi=_abi,)
        self.all_events_titles = self._get_contract_events_titles()
        self.last_block = self.contract.web3.eth.getBlock("latest").number
        self.blocks = []
        self.filters = []

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

    def _get_contract_events_titles(self) -> list:
        events = []
        for key, val in self.contract.events.__dict__.items():
            if key != "abi" and not key[0].startswith("_"):
                events.append(key)

        return events

    def _get_contract_event_by_title(self, contract_title: str) -> ContractEvent:
        return self.contract.events[contract_title]

    def _create_filter(
        self, contract_title: str, from_block: Union[str, int] = None, to_block: Union[str, int] = None,
    ) -> LogFilter:
        return self._get_contract_event_by_title(contract_title).createFilter(
            address=self.contract_address, fromBlock=from_block, toBlock=to_block
        )

    def _fetch_event_blocks_with_filter(self, event_filter: LogFilter, event: str = None) -> bool:
        try:
            for event in event_filter.get_all_entries():
                block = dict(contract=self.contract_meta.title, **self.serialize(event))
                self.blocks.append(block)
        except ConnectionClosedError as e:
            # TODO deal with exception code = 1011 (unexpected error), reason = Internal server disconnect error
            capture_exception(e)
            print(e, f"Contract:{self.contract_meta.title}", f"Event:{event}", sep="\n")
            pass

        return True

    def fetch_all_blocks(self):
        current_block = 6630000
        step = 10000

        while current_block < self.last_block:
            logging.info(
                f"FromBlock:{current_block}; ToBlock:{current_block + step}; TotalResult:{len(self.blocks)}"
            )
            for event in self.all_events_titles:
                self._fetch_event_blocks_with_filter(
                    self._create_filter(event, from_block=current_block, to_block=current_block + step)
                )

            current_block += step

        return True

    def fetch_blocks_from_block(self, from_block: Optional[int]) -> list:
        for event in self.all_events_titles:
            self._fetch_event_blocks_with_filter(
                self._create_filter(event, from_block=from_block), event
            ) if from_block else None
        return self.blocks

    async def save_blocks(self):
        tasks = [
            EthereumTransactionCRUD.update_or_create(
                transaction_hash=block["transactionHash"],
                log_index=block["logIndex"],
                payload=block
            ) for block in self.blocks
        ]
        await asyncio.gather(*tasks)
        return True

    async def fetch_blocks_and_save(self, from_block: Optional[int] = None):
        self.fetch_blocks_from_block(from_block) if from_block else self.fetch_all_blocks()
        print(f"{self.contract_meta.title}: {len(self.blocks)} new blocks")
        await self.save_blocks()
        return True
