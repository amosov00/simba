import httpx
from config import GASSTATION_URL, GASSTATION_API_TOKEN, ETH_MAX_GAS_PRICE_GWEI

__all__ = ["gasprice_from_ethgasstation"]


async def gasprice_from_ethgasstation() -> int:
    async with httpx.AsyncClient() as client:
        try:
            result = (
                await client.get(GASSTATION_URL, params={
                    "api-key": GASSTATION_API_TOKEN
                })
            ).json()
        except Exception:
            result = {}

    return int(result.get("fast", 0)) // 10
