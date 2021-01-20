from pydantic import Field
from sitri.settings.contrib.vault import VaultKVSettings

from config.provider import BaseSettingsConfig


class DBSettings(VaultKVSettings):
    uri: str = Field(...)
    name: str = Field(...)
    auth_source: str = Field(default="admin")

    class Config(BaseSettingsConfig):
        default_secret_path = "db"
        local_mode_path_prefix = "db"
