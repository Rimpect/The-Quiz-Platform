"""
Middleware для глобальной обработки ошибок
"""
import traceback
import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware для глобальной обработки ошибок"""

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response

        except HTTPException as http_exc:
            # HTTP исключения (400, 401, 403, 404 и т.д.)
            logger.warning(
                f"HTTP Exception: {http_exc.status_code} - {http_exc.detail} "
                f"Path: {request.url.path}"
            )

            # Форматируем ответ
            if http_exc.status_code == 401:
                status = "unauthorized"
                access_status = "missing"
            elif http_exc.status_code == 403:
                status = "forbidden"
                access_status = "denied"
            elif http_exc.status_code == 404:
                status = "not_found"
                access_status = "granted"
            else:
                status = "error"
                access_status = "denied"

            return JSONResponse(
                status_code=http_exc.status_code,
                content={
                    "status_code": http_exc.status_code,
                    "status": status,
                    "access_status": access_status,
                    "message": str(http_exc.detail),
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": None,
                    "errors": None
                }
            )

        except Exception as exc:
            # Необработанные исключения (500)
            error_id = str(hash(request))[:8]
            logger.error(
                f"Unhandled Exception [{error_id}]: {str(exc)}\n"
                f"{traceback.format_exc()}"
            )

            return JSONResponse(
                status_code=500,
                content={
                    "status_code": 500,
                    "status": "error",
                    "access_status": "denied",
                    "message": "Internal server error",
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": None,
                    "errors": {
                        "error_id": error_id,
                        "detail": str(exc) if logger.level == logging.DEBUG else None
                    }
                }
            )
        