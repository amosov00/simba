from .base import BlockCypherBaseAPIWrapper


class BlockCypherWebhooksWrapper(BlockCypherBaseAPIWrapper):
    async def create_webhook(self, data: dict) -> dict:
        endpoint = "/hooks"
        return await self.request(endpoint, "POST", data=data, with_token=True)

    async def list_webhooks(self) -> list:
        endpoint = "/hooks"
        return await self.request(endpoint, "GET", with_token=True)

    async def delete_webhook(self, webhook_id: str):
        endpoint = f"/hooks/${webhook_id}"
        return await self.request(endpoint, "DELETE", with_token=True)
