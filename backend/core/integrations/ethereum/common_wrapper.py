import asyncio
import logging
from typing import Optional, Union, List
from websockets import ConnectionClosedError
from datetime import datetime

from sentry_sdk import capture_exception

from .base_wrapper import EthereumBaseContractWrapper, EthereumBaseCommonWrapper
from schemas import EthereumTransaction
from database.crud import EthereumTransactionCRUD
from config import SIMBA_CONTRACT

__all__ = ['EthereumCommonWrapper']


class EthereumCommonWrapper(EthereumBaseCommonWrapper):
    def _create_filter(self, address: str, from_block: Union[str, int] = None, to_block: Union[str, int] = None):
        return self.w3.eth.filter({
            "address": SIMBA_CONTRACT.address, "fromBlock": from_block, "toBlock": to_block, "from": address
        })

    def _fetch_blocks(self, address, from_block: Union[str, int], to_block: Union[str, int]):
        for block in self._create_filter(address, from_block, to_block).get_all_entries():
            self.blocks.append(self.serialize(block))
            # self.blocks.append(EthereumTransaction(**block))

        return self.blocks

    def fetch_address_blocks(self, address: str, last_block: dict) -> list:
        pass

    def save_transations(self):
        pass
