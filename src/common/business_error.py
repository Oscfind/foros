from typing import Optional

from fastapi import HTTPException, status


class BusinessError(HTTPException):
    def __init__(
        self,
        detail: Optional[str] = None,
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
