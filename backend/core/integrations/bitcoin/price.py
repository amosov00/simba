from typing import Optional

from core.integrations.base import BaseApiWrapper

__all__ = ["BitcoinPriceWrapper"]


class BitcoinPriceWrapper(BaseApiWrapper):

    async def fetch_price_from_blockchain_info(self, raise_error: bool = True) -> Optional[float]:
        response = await self.request("https://blockchain.info/ticker", "GET", raise_error=raise_error)

        if response:
            return float(response["USD"]["15m"])

        return None

    async def fetch_price_from_coinconverter(self, raise_error: bool = True) -> Optional[float]:
        response = await self.request(
            "https://api.coinconvert.net/convert/btc/usd?amount=1",
            "GET",
            raise_error=raise_error
        )

        if response and response["status"] == "success":
            return float(response["USD"])

        return None

    async def fetch_bitcoin_price(self):
        return await self.fetch_price_from_blockchain_info(raise_error=False) or \
               await self.fetch_price_from_coinconverter(raise_error=True)
