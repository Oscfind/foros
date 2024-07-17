import os
from enum import StrEnum


class AppEnvironment(StrEnum):
    DEVELOPMENT = "Development"
    STAGING = "Staging"
    PRODUCTION = "Production"

    @staticmethod
    def get_current() -> str:
        return os.getenv("GLOBAL__ENVIRONMENT", AppEnvironment.DEVELOPMENT)