from http import HTTPStatus
from typing import Literal, Union
from urllib.parse import urlencode, urljoin

import httpx
from fastapi import HTTPException
from sentry_sdk import capture_message
from tenacity import retry, stop_after_attempt, wait_fixed


class BaseApiWrapper:
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
    async def request(
        self,
        url: str,
        request_type: Literal["GET", "POST", "DELETE"] = "GET",  # Noqa
        params: dict = None,
        data: dict = None,
    ) -> Union[list, dict, str, None]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            if request_type == "POST":
                if params:
                    url = urljoin(url, "?" + urlencode(params))

                resp = await client.post(url, json=data)

            elif request_type == "DELETE":
                resp = await client.delete(url, params=params)

            else:
                resp = await client.get(url, params=params)

        if resp.is_error:
            capture_message(
                f"Invalid request; status: {resp.status_code}; url: {url}; error {resp.text}",
                level="info"
            )
            raise HTTPException(HTTPStatus.BAD_REQUEST, resp.text)

        elif resp.text:
            return resp.json()
        else:
            return resp.text
