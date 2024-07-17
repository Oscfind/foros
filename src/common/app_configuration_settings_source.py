from typing import Any, Optional

from azure.appconfiguration import (
    AzureAppConfigurationClient,
    ConfigurationSetting,
    FeatureFlagConfigurationSetting,
    SecretReferenceConfigurationSetting,
)
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
)


class AppConfigurationSettingsSource(PydanticBaseSettingsSource):
    _credential: DefaultAzureCredential
    _app_configuration_client: AzureAppConfigurationClient

    def __init__(
        self, settings_cls: type[BaseSettings], connection_string: str
    ) -> None:
        self._credential = DefaultAzureCredential()
        self._app_configuration_client = AzureAppConfigurationClient(
            base_url=connection_string, credential=self._credential
        )
        super().__init__(settings_cls)

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> tuple[Any, str, bool]:
        field_value: Optional[Any] = None
        not_found_key = False
        configuration_setting: Optional[ConfigurationSetting] = None

        try:
            configuration_setting = (
                self._app_configuration_client.get_configuration_setting(key=field_name)  # type: ignore
            )
        except ResourceNotFoundError:
            not_found_key = True

        if not_found_key:
            field_value = None
        elif isinstance(configuration_setting, SecretReferenceConfigurationSetting):
            field_value = self._get_key_vault_field_value(configuration_setting)
        elif isinstance(configuration_setting, FeatureFlagConfigurationSetting):
            raise RuntimeError("Feature flags not supported")
        elif isinstance(configuration_setting, ConfigurationSetting):
            field_value = configuration_setting.value
        else:
            raise RuntimeError("Unknown configuration setting type")

        return field_value, field_name, False

    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        return value

    def __call__(self) -> dict[str, Any]:
        data: dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field, field_name
            )
            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex
            )

            if field_value is not None:
                data[field_key] = field_value

        return data

    def _get_key_vault_field_value(
        self, configuration_setting: ConfigurationSetting
    ) -> Optional[str]:
        secret_id: Optional[str] = configuration_setting.secret_id  # type: ignore

        if not isinstance(secret_id, Optional[str]):
            raise RuntimeError("Not valid type")

        if secret_id is None:
            raise RuntimeError("f{field_name} secret not assigned")

        key_vault_uri, secret_name = secret_id.split("/secrets/")
        client = SecretClient(vault_url=key_vault_uri, credential=self._credential)
        secret = client.get_secret(secret_name)  # type: ignore
        return secret.value