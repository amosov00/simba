import hvac
from sitri.providers.contrib.vault import VaultKVConfigProvider
from sitri.settings.contrib.vault import VaultKVSettings

from config.configurator import ENV, configurator, IS_LOCAL, local_mode_data_filename


def vault_client_factory() -> hvac.Client:
    client = hvac.Client(url=configurator.get("vault_api"))

    client.auth_approle(
        role_id=configurator.get("role_id"),
        secret_id=configurator.get("secret_id"),
    )

    return client


provider = VaultKVConfigProvider(
    vault_connector=vault_client_factory,
    mount_point=f"{configurator.get('envs_mount_point')}/{ENV}",
)


class BaseSettingsConfig(VaultKVSettings.VaultKVSettingsConfig):
    provider = provider

    local_mode = IS_LOCAL
    local_provider_args = {"json_path": local_mode_data_filename}
