"""Маппинг доменных исключений сервисного слоя в унифицированные HTTP-ответы.

Сервисы остаются HTTP-агностичными: кидают ServiceError, а конверт ответа
(тот же, что у ResponseFactory) собирается здесь централизованно.
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from ..schemas.schemas_response import ResponseFactory
from .exceptions import (
    ServiceError,
    BadRequestError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    ConflictError,
)


def _to_response(exc: ServiceError):
    if isinstance(exc, BadRequestError):
        return ResponseFactory.bad_request(message=exc.message, errors=exc.errors)
    if isinstance(exc, UnauthorizedError):
        return ResponseFactory.unauthorized(message=exc.message)
    if isinstance(exc, ForbiddenError):
        return ResponseFactory.forbidden(message=exc.message)
    if isinstance(exc, NotFoundError):
        return ResponseFactory.not_found(message=exc.message)
    if isinstance(exc, ConflictError):
        return ResponseFactory.conflict(message=exc.message, errors=exc.errors)
    return ResponseFactory.error(
        message=exc.message or "Internal server error",
        errors=exc.errors,
        status_code=exc.status_code,
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ServiceError)
    async def _handle_service_error(request: Request, exc: ServiceError):
        body = _to_response(exc)
        return JSONResponse(
            status_code=exc.status_code,
            content=body.model_dump(mode="json"),
        )
