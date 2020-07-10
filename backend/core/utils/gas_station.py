import httpx
from config import GAS_STATION_ENDPOINT


async def get_gas_price():
    async with httpx.AsyncClient() as client:
        gas_station_req = (await client.get(GAS_STATION_ENDPOINT)).json()

    gas_station_gwei = str(int(gas_station_req.get("fast")) // 10) if gas_station_req and gas_station_req.get(
        "fast") else "35"
    return gas_station_gwei
