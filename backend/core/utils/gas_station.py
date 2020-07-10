import httpx
from config import GAS_STATION_ENDPOINT, DEFAULT_GAS_PRICE


async def get_gas_price():
    async with httpx.AsyncClient() as client:
        try:
            gas_station_req = (await client.get(GAS_STATION_ENDPOINT)).json()
        except Exception:
            gas_station_req = None

    gas_station_gwei = str(int(gas_station_req.get("fast")) // 10) if gas_station_req and gas_station_req.get(
        "fast") else DEFAULT_GAS_PRICE
    print(gas_station_gwei)
    return gas_station_gwei
