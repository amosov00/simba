from http import HTTPStatus
from datetime import datetime, time

from bson import ObjectId, Decimal128, errors
from fastapi import HTTPException
from pydantic import BaseModel as PydanticBaseModel


class ObjectIdPydantic(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(v)
        except (errors.InvalidId, errors.InvalidBSON):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Invalid ID")


class DecimalPydantic(int):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, Decimal128):
            return int(v.to_decimal())
        else:
            return int(v)


class BaseModel(PydanticBaseModel):
    class Config:
        json_encoders = {
            ObjectId: lambda o: str(o),
            ObjectIdPydantic: lambda o: str(o),
            datetime: lambda o: o.isoformat(),
            time: lambda o: o.isoformat(),
            Decimal128: lambda o: int(o.to_decimal()),
        }
