from urllib.parse import urljoin

from config import settings, SIMBA_CONTRACT, IS_PRODUCTION
from .base import BaseApiWrapper

__all__ = ["EthplorerWrapper"]


class EthplorerWrapper(BaseApiWrapper):
    base_url = "https://api.ethplorer.io/"

    async def fetch_simba_metadata(self):
        if not IS_PRODUCTION:
            return {}
        url = urljoin(self.base_url, "/getTokenInfo/") + SIMBA_CONTRACT.address.lower()
        params = {"apiKey": settings.crypto.ethplorer_api_token}
        return await self.request(url, "GET", params)
