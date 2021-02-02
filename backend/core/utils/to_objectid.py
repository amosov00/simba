from fastapi import HTTPException
from starlette import status
from bson import errors, ObjectId

__all__ = ["to_objectid"]


def to_objectid(_id: str) -> ObjectId:
    try:
        return ObjectId(_id) if _id else None
    except (errors.InvalidId, errors.InvalidBSON):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid ID")
