from datetime import timedelta
from os import path

import sentry_sdk
from pydantic import BaseModel, Field

from schemas import EthereumContract, BTCxPub
from .config_parts import (
    CommonSettings,
    DBSettings,
    CryptoSettings,
    SentrySettings,
    EmailSettings,
    CelerySettings,
    KafkaSettings,
    PersonVerifySettings,
)
from .configurator import configurator, IS_LOCAL, IS_PRODUCTION, BASE_DIR


class AppSettings(BaseModel):
    db: DBSettings = Field(default_factory=DBSettings)
    common: CommonSettings = Field(default_factory=CommonSettings)
    sentry: SentrySettings = Field(default_factory=SentrySettings)
    crypto: CryptoSettings = Field(default_factory=CryptoSettings)
    email: EmailSettings = Field(default_factory=EmailSettings)
    celery: CelerySettings = Field(default_factory=CelerySettings)
    kafka: KafkaSettings = Field(default_factory=KafkaSettings)
    person_verify: PersonVerifySettings = Field(default_factory=PersonVerifySettings)


settings = AppSettings()

############################
# Sentry
############################
if settings.sentry.dsn and not IS_LOCAL:
    sentry_sdk.init(
        dsn=settings.sentry.dsn,
        environment=settings.common.environment,
        release=configurator.get("commit"),
        attach_stacktrace=True,
    )

############################
# ETH
############################
TRANSACTION_MIN_CONFIRMATIONS = 3 if IS_PRODUCTION else 1
GASSTATION_URL = "https://ethgasstation.info/api/ethgasAPI.json"
GASTRACKER_URL = "https://api.etherscan.io/api/"
SIMBA_BUY_SELL_FEE = 50000
SIMBA_MINIMAL_BUY_AMOUNT = 200000
ETH_MAX_GAS = 200000
ETH_MAX_GAS_PRICE_GWEI = 120

if IS_PRODUCTION:
    SIMBA_CONTRACT = EthereumContract(
        title="SIMBA",
        address="0x7806A1b2B6056cda57d3E889a9513615733E2B66",
        abi_filepath=path.join(BASE_DIR, "config", "simba_abi_mainnet.json"),
    )
    SST_CONTRACT = EthereumContract(
        title="SST",
        address="0x2863916C6ebDBBf0c6f02F87b7eB478509299868",
        abi_filepath=path.join(BASE_DIR, "config", "sst_abi_mainnet.json"),
    )

else:
    SIMBA_CONTRACT = EthereumContract(
        title="SIMBA",
        address="0x60E1BF648580AafbFf6c1bc122BB1AE6Be7C1352",
        abi_filepath=path.join(BASE_DIR, "config", "simba_abi_rinkeby.json"),
    )
    SST_CONTRACT = EthereumContract(
        title="SST",
        address="0xc17010e8d258631636827b3d8bac6830fc5163ff",
        abi_filepath=path.join(BASE_DIR, "config", "sst_abi_rinkeby.json"),
    )

############################
# BTC
############################

BTC_FEE = 10000
BTC_DECIMALS = 8

BTC_COLD_XPUB_UAE = BTCxPub(title="UAE", xpub=settings.crypto.btc_cold_xpub_uae, xpub_preview="")  # noqa
BTC_COLD_XPUB_LIECH = BTCxPub(title="Liechtenstein", xpub=settings.crypto.btc_cold_xpub_liech, xpub_preview="")  # noqa
BTC_COLD_XPUB_NEWZEL = BTCxPub(title="NewZealand", xpub=settings.crypto.btc_cold_xpub_newzel, xpub_preview="")  # noqa
BTC_COLD_XPUB_SWISS = BTCxPub(title="Switzerland", xpub=settings.crypto.btc_cold_xpub_swiss, xpub_preview="")  # noqa

BTC_COLD_WALLETS = (BTC_COLD_XPUB_UAE, BTC_COLD_XPUB_LIECH, BTC_COLD_XPUB_NEWZEL, BTC_COLD_XPUB_SWISS)

############################
# EMAIL
############################

SUPPORT_FREQUENCY_LIMIT = 10

############################
# INVOICE
############################

INVOICE_TIMEOUT = timedelta(hours=2)


class InvoiceVerificationLimits:
    LEVEL_1 = int(0.1 * 10 ** 8)     # Satoshi, Email verification, all time
    LEVEL_2 = int(2.0 * 10 ** 8) if IS_PRODUCTION else int(0.3 * 10 ** 8)    # Satoshi, KYC done, per month
