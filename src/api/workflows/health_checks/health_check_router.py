from fastapi import APIRouter, Response, status

router = APIRouter(prefix="", tags=["health-checks"])


@router.get("/")
def get_root_health_check() -> Response:
    return Response(status_code=status.HTTP_200_OK)


@router.get("/healthz")
def get_health_check() -> Response:
    return Response(status_code=status.HTTP_200_OK)