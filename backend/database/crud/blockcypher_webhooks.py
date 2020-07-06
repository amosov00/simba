from .base import BaseMongoCRUD

__all__ = ["BlockCypherWebhookCRUD"]


class BlockCypherWebhookCRUD(BaseMongoCRUD):
    collection = "webhook"

    @classmethod
    async def find_by_address(cls, address: str) -> list:
        return await super().find_many({"address": address})
