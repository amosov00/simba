from os import getenv, path

from .common import IS_PRODUCTION, BASE_DIR
from schemas import EthereumContract

BLOCKCYPHER_TOKEN = getenv("BLOCKCYPHER_TOKEN")
INFURA_HTTP_URL = getenv("INFURA_HTTP_URL")
INFURA_WS_URL = getenv("INFURA_WS_URL")

SIMBA_CONTRACT = EthereumContract(
    title="SIMBA",
    address="0x2e52216529F2C47735bbbB8D5fB868c4A93440c5",
    abi_filepath=path.join(BASE_DIR, "config", "simba_abi.json"),
    is_test=IS_PRODUCTION is False,
    provider_http_link=INFURA_HTTP_URL,
    provider_ws_link=INFURA_WS_URL
)
