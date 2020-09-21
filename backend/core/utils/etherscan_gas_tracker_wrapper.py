import httpx
from config import ETHERSCAN_API_TOKEN, ETH_MAX_GAS_PRICE_GWEI, GAS_TRACKER_URL

__all__ = ["gasprice_from_etherscan"]


async def gasprice_from_etherscan() -> int:
    async with httpx.AsyncClient() as client:
        try:
            result = (
                await client.get(GAS_TRACKER_URL, params={
                    "module": "gastracker",
                    "action": "gasoracle",
                    "apikey": ETHERSCAN_API_TOKEN,
                })
            ).json().get("result", {})
        except Exception:
            result = {}

    return int(result.get("ProposeGasPrice", 0))
