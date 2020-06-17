from http import HTTPStatus
from datetime import datetime, time
from hashlib import sha256

from bson import ObjectId, Decimal128, errors
from fastapi import HTTPException
from pydantic import BaseModel as PydanticBaseModel, Field
from web3 import Web3


def validate_eth_address(address_hash: str):
    status = False

    try:
        status = Web3.isAddress(address_hash)
    except:
        pass

    if not status:
        raise ValueError("Invalid ETH address")

    return address_hash


def validate_btc_address(address_hash: str):
    """ Origin: https://rosettacode.org/wiki/Bitcoin/address_validation#Python """

    def decode_base58(bc, length):
        n = 0
        for char in bc:
            n = n * 58 + chars.index(char)
        return n.to_bytes(length, 'big')

    chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    status = False

    try:
        bcbytes = decode_base58(address_hash, 25)
        status = bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]
    except:
        pass

    if not status:
        raise ValueError("Invalid BTC address")

    return address_hash


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
