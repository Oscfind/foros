from logging import Logger

from fastapi import HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from src.api.common.dependency_container import DependencyContainer


class ExceptionMiddleware(BaseHTTPMiddleware):
    _logger: Logger

    def __init__(self, app: ASGIApp) -> None:
        self._logger = DependencyContainer.get_logger()
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            return await call_next(request)
        except Exception as e:
            if not isinstance(e, HTTPException):
                self._logger.exception(e)

            raise
