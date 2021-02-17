from pydantic import Field
from sitri.settings.contrib.vault import VaultKVSettings

from config.provider import BaseSettingsConfig


class PersonVerifySettings(VaultKVSettings):
    app_token: str = Field(...)
    secret_key: str = Field(...)
    base_url: str = Field(...)
    status_webhook_secret_key: str = Field(...)

    class Config(BaseSettingsConfig):
        default_secret_path = "person_verify"
        local_mode_path_prefix = "person_verify"
