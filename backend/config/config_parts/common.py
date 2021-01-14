from os import getenv, path

from pydantic import Field
from sitri.settings.contrib.vault import VaultKVSettings

from config.configurator import ENV
from config.provider import BaseSettingsConfig

BASE_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
VERSION = getenv("VERSION")
COMMIT = getenv("COMMIT")

DEBUG = getenv("DEBUG", "") == "True"
IS_PRODUCTION = ENV == "production"

ALLOWED_ORIGINS = ["*"]


class CommonSettings(VaultKVSettings):
    title: str = Field(...)
    environment: str = Field(default=ENV)
    host_url: str = Field(default=None)
    secret: str = Field(...)
    debug: bool = Field(default=False)
    support_email: str = Field(...)

    class Config(BaseSettingsConfig):
        default_secret_path = "common"
        local_mode_path_prefix = "common"
