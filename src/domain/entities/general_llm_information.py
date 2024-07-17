from pydantic import BaseModel

from src.domain.entities.model_information import ModelInformation


class GeneralLLMInformation(BaseModel):
    heavy: ModelInformation
    light: ModelInformation