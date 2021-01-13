from pydantic import Field
from sitri.settings.contrib.vault import VaultKVSettings

from config.provider import BaseSettingsConfig


class CryptoSettings(VaultKVSettings):
    infura_http_url: str = Field(...)
    infura_ws_url: str = Field(...)

    gasstation_api_token: str = Field(...)
    etherscan_api_token: str = Field(...)
    ethplorer_api_token: str = Field(...)

    blockcypher_token: str = Field(...)
    blockcypher_wallet_title: str = Field(...)

    simba_admin_address: str = Field(...)
    simba_admin_private_key: str = Field(...)

    btc_hot_wallet_address: str = Field(...)
    btc_hot_wallet_wif: str = Field(...)

    btc_multisig_wallet_address: str = Field(...)
    btc_multisig_cosig_1_wif: str = Field(...)
    btc_multisig_cosig_2_pub: str = Field(...)

    btc_cold_xpub_swiss: str = Field(...)
    btc_cold_xpub_liech: str = Field(...)
    btc_cold_xpub_newzel: str = Field(...)
    btc_cold_xpub_uae: str = Field(...)

    class Config(BaseSettingsConfig):
        default_secret_path = "crypto"
        local_mode_path_prefix = "crypto"
