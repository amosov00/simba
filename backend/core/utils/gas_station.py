import httpx
from config import GASSTATION_API_TOKEN, DEFAULT_GAS_PRICE

GASSTATION_URL = "https://ethgasstation.info/api/ethgasAPI.json?api-key="


async def gas_price_from_ethgasstation() -> str:
    async with httpx.AsyncClient() as client:
        try:
            gas_station_req = (await client.get(GASSTATION_URL + GASSTATION_API_TOKEN)).json()
        except Exception:
            gas_station_req = None

    gas_station_gwei = str(int(gas_station_req.get("fast")) // 10) \
        if gas_station_req and gas_station_req.get("fast") \
        else DEFAULT_GAS_PRICE

    return gas_station_gwei
