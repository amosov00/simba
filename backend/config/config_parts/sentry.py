from pydantic import Field
from sitri.settings.contrib.vault import VaultKVSettings

from config.provider import BaseSettingsConfig


class SentrySettings(VaultKVSettings):
    enable: bool = Field(default=True)
    dsn: str = Field(...)
    trace_rate: float = Field(default=1.0)

    class Config(BaseSettingsConfig):
        default_secret_path = "sentry"
        local_mode_path_prefix = "sentry"
