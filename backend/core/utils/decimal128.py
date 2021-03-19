from decimal import Decimal
from typing import Union, Optional

from bson import Decimal128

__all__ = ["to_decimal128", "from_decimal128"]


def to_decimal128(val: Union[int, Decimal, Decimal128, None]) -> Optional[Decimal128]:
    if isinstance(val, int):
        return Decimal128(Decimal(val))
    elif isinstance(val, Decimal):
        return Decimal128(val)
    else:
        return val


def from_decimal128(val: Union[int, Decimal, Decimal128]) -> int:
    if isinstance(val, Decimal128):
        return int(val.to_decimal())
    elif val is not None:
        return int(val)
    else:
        return val
