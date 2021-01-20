from motor import motor_asyncio

from config import settings

__all__ = ["mongo"]


class Mongo:
    def __init__(self):
        self._client = motor_asyncio.AsyncIOMotorClient(
            settings.db.uri, authSource=settings.db.auth_source, connect=True
        )
        self._db = self._client[settings.db.name]

    @property
    def db(self):
        return self._db

    @property
    def client(self):
        return self._client

    def close(self):
        self._client.close()


mongo = Mongo()
