from pydantic import BaseModel

class ModelInformation(BaseModel):
    provider: str
    deployment_name: str