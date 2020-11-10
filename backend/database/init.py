from motor import motor_asyncio

from config import MONGO_DATABASE_URL, MONGO_DATABASE_NAME

__all__ = ["mongo"]


class Mongo:
    def __init__(self):
        self._client = motor_asyncio.AsyncIOMotorClient(
            MONGO_DATABASE_URL, connect=True
        )
        self._db = self._client[MONGO_DATABASE_NAME]

    @property
    def db(self):
        return self._db

    async def ping(self):
        return await self.client.admin.command("ping")

    @property
    def client(self):
        return self._client

    def close(self):
        self._client.close()


mongo = Mongo()
