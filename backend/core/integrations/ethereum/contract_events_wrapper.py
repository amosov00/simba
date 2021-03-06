import asyncio
from datetime import datetime
from typing import Optional, Union, List

from sentry_sdk import capture_exception
from web3.contract import LogFilter
from websockets import ConnectionClosedError

from database.crud import EthereumTransactionCRUD
from .base_wrapper import EthereumBaseContractWrapper

__all__ = ["EventsContractWrapper"]


class EventsContractWrapper(EthereumBaseContractWrapper):
    def _create_filter(
        self,
        contract_title: str,
        from_block: Union[str, int] = None,
        to_block: Union[str, int] = None,
    ) -> LogFilter:
        return self._get_contract_event_by_title(contract_title).createFilter(
            address=self.contract_address, fromBlock=from_block, toBlock=to_block
        )

    def _fetch_event_blocks_with_filter(self, event_filter: LogFilter) -> bool:
        """
        # TODO deal with Infura API bug: getEventFilters
        try:
            for event in event_filter.get_all_entries():
                block = self.serialize(event)
                self.blocks.append(
                    EthereumTransaction(**block, contract=self.contract_meta.title, fetched_at=datetime.now())
                )
        except ConnectionClosedError as e:
            # TODO deal with exception code = 1011 (unexpected error), reason = Internal server disconnect error
            capture_exception(e)
            logging.error(e, f"Contract:{self.contract_meta.title}", f"Event:{event}", sep="\n")
        """
        log_entries = event_filter._filter_valid_entries(  # noqa
            event_filter.web3.eth.getLogs(event_filter.filter_params)
        )
        try:
            for event in event_filter._format_log_entries(log_entries):  # noqa
                transaction = self.serialize(event)
                transaction.update({
                    "confirmations": self.last_block - transaction["blockNumber"],
                    "contract": self.contract_meta.title,
                    "fetched_at": datetime.now()
                })
                self.transactions.append(transaction)

        except ConnectionClosedError as e:
            capture_exception(e)

        return True

    def fetch_all_blocks(self):
        current_block = 6630000
        step = 1000000
        while current_block < self.last_block:
            for event in self.contract_events:
                self._fetch_event_blocks_with_filter(
                    self._create_filter(event, from_block=current_block, to_block=current_block + step)
                )
            print(f"FromBlock:{current_block}; ToBlock:{current_block + step}; TotalResult:{len(self.transactions)}")
            current_block += step

        return True

    def fetch_blocks_from_block(self, from_block: Optional[int]) -> list:
        for event in self.contract_events:
            self._fetch_event_blocks_with_filter(
                self._create_filter(event, from_block=from_block)
            ) if from_block else None
        return self.transactions

    async def save_transactions(self):
        tasks = [
            EthereumTransactionCRUD.update_or_insert(
                query={
                    "transactionHash": block["transactionHash"],
                    "logIndex": block["logIndex"],
                    "transactionIndex": block["transactionIndex"],
                },
                payload=block,
            )
            for block in list(filter(lambda o: o["confirmations"] >= self.min_confirmations, self.transactions))
        ]
        async with asyncio.Semaphore(25):
            await asyncio.gather(*tasks)
        return True

    async def find_or_save_transactions(self):
        tasks = [
            EthereumTransactionCRUD.update_or_insert(
                query={
                    "transactionHash": block["transactionHash"],
                    "logIndex": block["logIndex"],
                    "transactionIndex": block["transactionIndex"],
                },
                payload=block,
            )
            for block in list(filter(lambda o: o["confirmations"] >= self.min_confirmations, self.transactions))
        ]

        async with asyncio.Semaphore(100):
            await asyncio.gather(*tasks)
        return True

    async def fetch_blocks(self, from_block: Optional[int] = None) -> List[dict]:
        if not from_block:
            last_block = await EthereumTransactionCRUD.find_last_block(self.contract_meta.title)
            from_block = last_block.get("blockNumber") if last_block else None

        self.fetch_blocks_from_block(from_block + 1) if from_block else self.fetch_all_blocks()
        return self.transactions

    async def fetch_blocks_and_save(self, from_block: Optional[int] = None) -> List[dict]:
        await self.fetch_blocks(from_block)
        await self.save_transactions()
        return self.transactions

    async def fetch_missing_blocks(self):
        self.fetch_all_blocks()
        await self.find_or_save_transactions()
        return True
