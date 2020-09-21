import httpx
from config import ETHERSCAN_API_TOKEN, ETH_MAX_GAS_PRICE_GWEI, GAS_TRACKER_URL

__all__ = ["gas_price_from_ethgasstation"]


async def gas_price_from_ethgasstation() -> int:
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

    gas_price = result.get("ProposeGasPrice", ETH_MAX_GAS_PRICE_GWEI)

    # Filter dangerous gas price
    return min(gas_price, ETH_MAX_GAS_PRICE_GWEI)
