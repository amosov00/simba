from typing import Optional, Tuple, Union

from pydantic import HttpUrl

from .base import BaseModel

__all__ = ["EthereumContract"]


class EthereumContract(BaseModel):
    title: str = None
    address: str = None
    abi: Optional[list] = None
    abi_filepath: Optional[str] = None
    first_block: int = None
    is_test: bool = False
    provider_http_link: HttpUrl = None
    provider_ws_link: HttpUrl = None
