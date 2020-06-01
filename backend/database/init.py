from motor import motor_asyncio

from config import MONGO_DATABASE_URL, MONGO_DATABASE_NAME

__all__ = ["mongo_db", "mongo_client"]


class Mongo:
    def __init__(self):
        self._client = motor_asyncio.AsyncIOMotorClient(MONGO_DATABASE_URL, connect=True)
        self._db = self._client[MONGO_DATABASE_NAME]

    @property
    def db(self):
        return self._db

    @property
    def client(self):
        return self._client

    def close(self):
        self._client.close()


mongo_instanse = Mongo()
mongo_client = mongo_instanse.client
mongo_db = mongo_instanse.db
