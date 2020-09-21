import httpx
from config import GASSTATION_URL, GASSTATION_API_TOKEN, ETH_MAX_GAS_PRICE_GWEI


async def gas_price_from_ethgasstation() -> int:
    async with httpx.AsyncClient() as client:
        try:
            gas_station_req = (
                await client.get(GASSTATION_URL, params={
                    "api-key": GASSTATION_API_TOKEN
                })
            ).json()
        except Exception:
            gas_station_req = None

    gas_station_gwei = (
        int(gas_station_req.get("fast") // 10)
        if gas_station_req and gas_station_req.get("fast")
        else ETH_MAX_GAS_PRICE_GWEI
    )

    # Filter dangerous gas price
    return min(gas_station_gwei, ETH_MAX_GAS_PRICE_GWEI)
