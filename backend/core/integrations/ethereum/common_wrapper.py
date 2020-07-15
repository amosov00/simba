from typing import Union

from config import SIMBA_CONTRACT
from .base_wrapper import EthereumBaseCommonWrapper

__all__ = ["EthereumCommonWrapper"]


class EthereumCommonWrapper(EthereumBaseCommonWrapper):
    # TODO deprecated, delete after 10/07/2020
    def _create_filter(
        self, address: str, from_block: Union[str, int] = None, to_block: Union[str, int] = None
    ):
        return self.w3.eth.filter(
            {"address": SIMBA_CONTRACT.address, "fromBlock": from_block, "toBlock": to_block, "from": address}
        )

    def _fetch_blocks(self, address, from_block: Union[str, int], to_block: Union[str, int]):
        for block in self._create_filter(address, from_block, to_block).get_all_entries():
            self.blocks.append(self.serialize(block))
            # self.blocks.append(EthereumTransaction(**block))

        return self.blocks

    def fetch_address_blocks(self, address: str, last_block: dict) -> list:
        pass

    def save_transations(self):
        pass
