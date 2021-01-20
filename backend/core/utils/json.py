import json
from datetime import datetime, date
from typing import Any

import ujson
from bson import ObjectId, Decimal128
from starlette.responses import JSONResponse

__all__ = ["CustomEncoder", "CustomJSONResponse"]


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, date) or isinstance(o, datetime):
            return o.ctime()
        elif isinstance(o, Decimal128):
            return int(o.to_decimal())

        return ujson.dumps(o)


class CustomJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            cls=CustomEncoder,
        ).encode("utf-8")
