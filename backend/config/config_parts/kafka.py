from typing import Optional

from pydantic import Field
from sitri.settings.contrib.vault import VaultKVSettings

from config.provider import BaseSettingsConfig


class KafkaSettings(VaultKVSettings):
    app_name: str = Field(...)
    server: str = Field(...)
    sasl_enable: bool = Field(default=False)
    sasl_username: Optional[str] = Field(default=None)
    sasl_password: Optional[str] = Field(default=None)

    class Config(BaseSettingsConfig):
        default_secret_path = "kafka"
        local_mode_path_prefix = "kafka"
