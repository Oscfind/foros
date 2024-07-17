import os

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from src.common.app_configuration_settings_source import AppConfigurationSettingsSource
from src.common.app_environment import AppEnvironment

class ApplicationSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=[".env", f".env.{AppEnvironment.get_current()}"],
    )

    # @classmethod
    # def settings_customise_sources(
    #     cls,
    #     settings_cls: type[BaseSettings],
    #     init_settings: PydanticBaseSettingsSource,
    #     env_settings: PydanticBaseSettingsSource,
    #     dotenv_settings: PydanticBaseSettingsSource,
    #     file_secret_settings: PydanticBaseSettingsSource,
    # ) -> tuple[PydanticBaseSettingsSource, ...]:
    #     return (
    #         env_settings,
    #         dotenv_settings,
    #         AppConfigurationSettingsSource(
    #             settings_cls, os.environ["APP_CONFIGURATION__ENDPOINT"]
    #         ),
    #     )

    # GLOBAL__ENVIRONMENT: str
    # GLOBAL__SECURITY__JWT__KEY: str
    # GLOBAL__SECURITY__JWT__ALGORITHM: str
    # GLOBAL__SECURITY__JWT__ISSUER: str
    # GLOBAL__SECURITY__JWT__AUDIENCE: str

    # SQL_SERVER__CONNECTION_STRING: str

    # OPEN_AI_EMBEDDINGS__API_TYPE: str
    # OPEN_AI_EMBEDDINGS__API_KEY: str
    # OPEN_AI_EMBEDDINGS__AZURE_ENDPOINT: str
    # OPEN_AI_EMBEDDINGS__API_VERSION: str

    # QDRANT__ENDPOINT: str
    # QDRANT__API_KEY: str
    # QDRANT__PORT: int
    # QDRANT__EMBEDDING_ENGINE_NAME: str

    OPEN_AI__API_KEY: str
    OPEN_AI__AZURE_ENDPOINT: str = ""
    OPEN_AI__API_VERSION: str = ""

    # OPEN_AI__OAI_API_KEY: str

    # LLM__INFORMATION_HEAVY: str
    # LLM__INFORMATION_LIGHT: str

    # EMBEDDING__PROVIDER: str

    # GOOGLE__REGION: str
    # GOOGLE__API_KEY: str

    # APPLICATION_INSIGHTS__CONNECTION_STRING: str

    # IA_PREPARADOR__LOG_LEVEL: str