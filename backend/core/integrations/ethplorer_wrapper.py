from urllib.parse import urljoin

from config.crypto import ETHPLORER_API_TOKEN, IS_PRODUCTION
from .base import BaseApiWrapper

__all__ = ["EthplorerWrapper"]


class EthplorerWrapper(BaseApiWrapper):
    base_url = "https://api.ethplorer.io/"
    api_key = ETHPLORER_API_TOKEN

    async def fetch_simba_metadata(self):
        if not IS_PRODUCTION:
            return {}
        url = urljoin(self.base_url, "/getTokenInfo/") + "0x7806a1b2b6056cda57d3e889a9513615733e2b66"
        params = {"apiKey": self.api_key}
        return await self.request(url, "GET", params)
