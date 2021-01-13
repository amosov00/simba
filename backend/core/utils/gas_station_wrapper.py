import httpx

from config import GASSTATION_URL, settings

__all__ = ["gasprice_from_ethgasstation"]


async def gasprice_from_ethgasstation() -> int:
    async with httpx.AsyncClient() as client:
        try:
            result = (await client.get(GASSTATION_URL, params={"api-key": settings.crypto.gasstation_api_token})).json()
        except Exception:
            result = {}

    return int(result.get("fast", 0)) // 10
