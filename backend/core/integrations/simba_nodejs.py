import httpx

from fastapi import status, HTTPException
from sentry_sdk import capture_message

__all__ = ["SimbaNodeJSWrapper"]


class SimbaNodeJSWrapper:
    base_url = "http://backend-nodejs:8080/api"

    @classmethod
    async def fetch_multisig_transaction(cls, data: dict):
        endpoint = "/multisig"
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(cls.base_url + endpoint, json=data)
            except Exception as e:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))

        if resp.status_code != 200:
            capture_message("Error while creating transaction")
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Error while creating transaction")

        return resp.json()
