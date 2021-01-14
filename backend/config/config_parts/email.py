from pydantic import Field
from sitri.settings.contrib.vault import VaultKVSettings

from config.provider import BaseSettingsConfig


class EmailSettings(VaultKVSettings):
    email_login: str = Field(...)
    email_password: str = Field(...)
    email_port: str = Field(...)
    email_server: str = Field(...)

    mailgun_api_key: str = Field(...)
    mailgun_domain_name: str = Field(...)
    mailgun_message_link: str = Field(...)

    class Config(BaseSettingsConfig):
        default_secret_path = "email"
        local_mode_path_prefix = "email"
