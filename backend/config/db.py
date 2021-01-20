from os import getenv

MONGO_DATABASE_URL = getenv("DATABASE_URL") or "mongodb://localhost:27017"
MONGO_DATABASE_NAME = getenv("DATABASE_NAME") or "db"
