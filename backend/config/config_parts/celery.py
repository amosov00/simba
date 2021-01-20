from pydantic import Field
from sitri.settings.contrib.vault import VaultKVSettings

from config.provider import BaseSettingsConfig


class CelerySettings(VaultKVSettings):
    celery_broker_url: str = Field(...)

    class Config(BaseSettingsConfig):
        default_secret_path = "celery"
        local_mode_path_prefix = "celery"
