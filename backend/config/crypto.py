from os import getenv, path

from .common import IS_PRODUCTION, BASE_DIR
from schemas import EthereumContract

BLOCKCYPHER_TOKEN = getenv("BLOCKCYPHER_TOKEN")
BLOCKCYPHER_WALLET_TITLE = getenv("BLOCKCYPHER_WALLET_TITLE", "test1")
INFURA_HTTP_URL = getenv("INFURA_HTTP_URL")
INFURA_WS_URL = getenv("INFURA_WS_URL")

SIMBA_CONTRACT = EthereumContract(
    title="SIMBA",
    address="0x60E1BF648580AafbFf6c1bc122BB1AE6Be7C1352",
    abi_filepath=path.join(BASE_DIR, "config", "simba_abi.json"),
    is_test=IS_PRODUCTION is False,
    provider_http_link=INFURA_HTTP_URL,
    provider_ws_link=INFURA_WS_URL
)
