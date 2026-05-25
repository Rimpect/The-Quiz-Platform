import traceback
import logging
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Union

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware) :
    """Middleware для глобальной обработки ошибок"""

    async def dispatch(self, request: Request, call_next) :
        try :
            response = await call_next(request)
            return response

        except HTTPException as http_exc :
            # HTTP исключения (400, 401, 403, 404 и т.д.)
            logger.warning(
                f"HTTP Exception: {http_exc.status_code} - {http_exc.detail} "
                f"Path: {request.url.path}"
            )
            return JSONResponse(
                status_code=http_exc.status_code,
                content={"detail" : http_exc.detail}
            )

        except Exception as exc :
            # Необработанные исключения (500)
            error_id = str(hash(request))[:8]
            logger.error(
                f"Unhandled Exception [{error_id}]: {str(exc)}\n"
                f"{traceback.format_exc()}"
            )

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail" : "Internal server error",
                    "error_id" : error_id
                }
            )


class ValidationErrorMiddleware(BaseHTTPMiddleware) :
    """Middleware для обработки ошибок валидации Pydantic"""

    async def dispatch(self, request: Request, call_next) :
        from pydantic import ValidationError

        try :
            response = await call_next(request)
            return response

        except ValidationError as exc :
            logger.warning(f"Validation error: {exc.errors()}")
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"detail" : exc.errors()}
            )