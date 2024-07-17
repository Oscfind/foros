from src.api.workflows.contenidos_azure.request_content import SchemaRequest
from src.api.common.dependency_container import DependencyContainer
from fastapi import APIRouter, Response


router = APIRouter(prefix="/contenidos", tags=["contenidos"])

@router.post("/schema_generator/")
async def generate_schema(request: SchemaRequest) -> Response:
    return DependencyContainer.get_schema_generator_workflow().execute(request)