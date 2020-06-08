from .base import BaseMongoCRUD


class DebugCRUD(BaseMongoCRUD):
    collection = 'debug'
