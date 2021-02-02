import abc
from datetime import datetime
from io import BytesIO
from typing import Iterable

import ujson
import xlsxwriter
from bson import Decimal128


class BaseExcelWriter(metaclass=abc.ABCMeta):
    def __init__(self, data):
        self.start_row = 0
        self.start_col = 0
        self.output = BytesIO()
        self.wb = xlsxwriter.Workbook(self.output, {"in_memory": True})
        self.ws = self.wb.add_worksheet()
        self.data = data
        self.header_map = {}

        self.bold = self.wb.add_format({"bold": True})

    def _write_header(self, keys, x: int, y: int, level: int, exclude_keys: Iterable = None) -> int:
        if not exclude_keys:
            exclude_keys = []

        if level not in self.header_map.keys():
            self.header_map[level] = {}

        for key in keys:
            if key in exclude_keys or key in self.header_map[level].keys():
                continue

            self.ws.write_string(x, y, key, self.bold)
            self.header_map[level][key] = y
            y += 1

        return y

    def _write_row(self, data: dict, x: int, level: int, exclude_keys: Iterable = None):
        for key, val in data.items():
            if exclude_keys and key in exclude_keys:
                continue

            if isinstance(val, Decimal128):
                val = int(val.to_decimal())
            if "timestamp" in key or "date" in key or key == "created_at":
                if isinstance(val, int):
                    val = datetime.fromtimestamp(val).isoformat()
                else:
                    val = str(val)
            elif "id" in key:
                val = str(val)

            elif isinstance(val, (list, dict)):
                val = ujson.dumps(val)

            self.ws.write(x, self.header_map[level][key], val)

        return True

    @abc.abstractmethod
    def proceed(self):
        pass
