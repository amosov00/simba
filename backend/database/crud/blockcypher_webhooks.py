from .base import BaseMongoCRUD

__all__ = ['BlockCypherWebhookCRUD']


class BlockCypherWebhookCRUD(BaseMongoCRUD):
    collection = "webhook"

    def find_by_address(self, address: str) -> list:
        return await super().find_many({"address": address})
