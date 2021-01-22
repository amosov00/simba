from typing import Optional

from .base import BaseModel, Field

__all__ = ["EthereumContract", "EthereumContractMetaResponse"]


class EthereumContract(BaseModel):
    title: str = None
    address: str = None
    abi: Optional[list] = None
    abi_filepath: Optional[str] = None
    first_block: int = None


class EthereumContractResponse(BaseModel):
    title: str = None
    address: str = None
    abi: Optional[list] = None


class EthereumContractMetaResponse(BaseModel):
    contract: EthereumContractResponse = Field(...)
    provider_http_link: str = None
    provider_ws_link: str = None
