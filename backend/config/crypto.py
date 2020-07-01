from os import getenv, path

from .common import IS_PRODUCTION, BASE_DIR
from schemas import EthereumContract

BLOCKCYPHER_TOKEN = getenv("BLOCKCYPHER_TOKEN")
BLOCKCYPHER_WALLET_TITLE = getenv("BLOCKCYPHER_WALLET_TITLE", "test2")
INFURA_HTTP_URL = getenv("INFURA_HTTP_URL")
INFURA_WS_URL = getenv("INFURA_WS_URL")

SIMBA_ADMIN_ADDRESS = getenv("SIMBA_ADMIN_ADDRESS")
SIMBA_ADMIN_PRIVATE_KEY = getenv("SIMBA_ADMIN_PRIVATE_KEY")

SST_ADMIN_ADDRESS = getenv("SST_ADMIN_ADDRESS")
SST_ADMIN_PRIVATE_KEY = getenv("SST_ADMIN_PRIVATE_KEY")

BTC_HOT_WALLET_ADDRESS = getenv("BTC_HOT_WALLET_ADDRESS")
BTC_HOT_WALLET_WIF = getenv("BTC_HOT_WALLET_WIF")
BTC_MINIMAL_CONFIRMATIONS = 3 if IS_PRODUCTION else 1

if IS_PRODUCTION:
    pass

else:
    SIMBA_CONTRACT = EthereumContract(
        title="SIMBA",
        address="0x60E1BF648580AafbFf6c1bc122BB1AE6Be7C1352",
        abi_filepath=path.join(BASE_DIR, "config", "simba_abi_rinkeby.json"),
        is_test=IS_PRODUCTION is False,
        provider_http_link=INFURA_HTTP_URL,
        provider_ws_link=INFURA_WS_URL
    )
    SST_CONTRACT = EthereumContract(
        title="SST",
        address="0xc17010e8d258631636827b3d8bac6830fc5163ff",
        abi_filepath=path.join(BASE_DIR, "config", "sst_abi_rinkeby.json"),
        is_test=IS_PRODUCTION is False,
        provider_http_link=INFURA_HTTP_URL,
        provider_ws_link=INFURA_WS_URL
    )