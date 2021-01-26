import httpx

from config import GASTRACKER_URL, settings

__all__ = ["gasprice_from_etherscan"]


async def gasprice_from_etherscan() -> int:
    async with httpx.AsyncClient() as client:
        try:
            result = (
                await client.get(
                    GASTRACKER_URL,
                    params={
                        "module": "gastracker",
                        "action": "gasoracle",
                        "apikey": settings.crypto.etherscan_api_token,
                    },
                )
            ).json()
        except Exception:
            result = {}

    if result.get("status") == 0:
        return 0

    return int(result.get("result", {}).get("ProposeGasPrice", 0))
