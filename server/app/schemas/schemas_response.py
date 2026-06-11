"""
Базовые схемы для унифицированных ответов API
"""
from datetime import datetime
from enum import Enum
from typing import Optional, Any, Dict, List, TypeVar

from pydantic import BaseModel, Field


class AccessStatus(str, Enum):
    """Статус доступа"""
    GRANTED = "granted"
    DENIED = "denied"
    EXPIRED = "expired"
    MISSING = "missing"
    GUEST = "guest"


class ResponseStatus(str, Enum):
    """HTTP статусы в читаемом виде"""
    SUCCESS = "success"
    CREATED = "created"
    ACCEPTED = "accepted"
    BAD_REQUEST = "bad_request"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    ERROR = "error"


T = TypeVar('T')


class BaseResponse(BaseModel):
    """Базовый шаблон для всех ответов API"""
    status_code: int = Field(..., description="HTTP статус код")
    status: ResponseStatus = Field(..., description="Статус в читаемом виде")
    access_status: AccessStatus = Field(..., description="Статус доступа")
    message: str = Field(..., description="Информационное сообщение")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Время ответа")
    data: Optional[Any] = Field(None, description="Основные данные ответа")
    errors: Optional[Dict[str, Any]] = Field(None, description="Ошибки валидации")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class PaginatedResponse(BaseResponse):
    """Ответ с пагинацией"""
    data: Optional[Dict[str, Any]] = Field(None, description="Данные с пагинацией")

    class Config:
        json_schema_extra = {
            "example": {
                "status_code": 200,
                "status": "success",
                "access_status": "granted",
                "message": "Список получен успешно",
                "timestamp": "2024-01-01T12:00:00",
                "data": {
                    "items": [],
                    "total": 100,
                    "page": 1,
                    "size": 10,
                    "pages": 10
                },
                "errors": None
            }
        }


class ErrorResponse(BaseResponse):
    """Ответ с ошибкой"""
    status_code: int = Field(400, description="HTTP статус код")
    status: ResponseStatus = Field(ResponseStatus.ERROR, description="Статус")
    message: str = Field(..., description="Сообщение об ошибке")

    class Config:
        json_schema_extra = {
            "example": {
                "status_code": 400,
                "status": "error",
                "access_status": "denied",
                "message": "Ошибка валидации",
                "timestamp": "2024-01-01T12:00:00",
                "data": None,
                "errors": {
                    "email": "Invalid email format"
                }
            }
        }


class ResponseFactory:
    """Фабрика для создания унифицированных ответов"""

    @staticmethod
    def success(
            data: Any = None,
            message: str = "Operation completed successfully",
            access_status: AccessStatus = AccessStatus.GRANTED
    ) -> BaseResponse:
        return BaseResponse(
            status_code=200,
            status=ResponseStatus.SUCCESS,
            access_status=access_status,
            message=message,
            data=data
        )

    @staticmethod
    def created(
            data: Any = None,
            message: str = "Resource created successfully",
            access_status: AccessStatus = AccessStatus.GRANTED
    ) -> BaseResponse:
        return BaseResponse(
            status_code=201,
            status=ResponseStatus.CREATED,
            access_status=access_status,
            message=message,
            data=data
        )

    @staticmethod
    def bad_request(
            message: str = "Bad request",
            errors: Dict[str, Any] = None,
            access_status: AccessStatus = AccessStatus.DENIED
    ) -> BaseResponse:
        return BaseResponse(
            status_code=400,
            status=ResponseStatus.BAD_REQUEST,
            access_status=access_status,
            message=message,
            errors=errors
        )

    @staticmethod
    def unauthorized(
            message: str = "Authentication required",
            access_status: AccessStatus = AccessStatus.MISSING
    ) -> BaseResponse:
        """

        :rtype: object
        """
        return BaseResponse(
            status_code=401,
            status=ResponseStatus.UNAUTHORIZED,
            access_status=access_status,
            message=message
        )

    @staticmethod
    def forbidden(
            message: str = "Access forbidden",
            access_status: AccessStatus = AccessStatus.DENIED
    ) -> BaseResponse:
        return BaseResponse(
            status_code=403,
            status=ResponseStatus.FORBIDDEN,
            access_status=access_status,
            message=message
        )

    @staticmethod
    def not_found(
            message: str = "Resource not found",
            resource: str = None
    ) -> BaseResponse:
        if resource:
            message = f"{resource} not found"
        return BaseResponse(
            status_code=404,
            status=ResponseStatus.NOT_FOUND,
            access_status=AccessStatus.GRANTED,
            message=message
        )

    @staticmethod
    def conflict(
            message: str = "Resource already exists",
            errors: Dict[str, Any] = None
    ) -> BaseResponse:
        return BaseResponse(
            status_code=409,
            status=ResponseStatus.CONFLICT,
            access_status=AccessStatus.GRANTED,
            message=message,
            errors=errors
        )

    @staticmethod
    def error(
            message: str = "Internal server error",
            errors: Dict[str, Any] = None,
            status_code: int = 500
    ) -> BaseResponse:
        return BaseResponse(
            status_code=status_code,
            status=ResponseStatus.ERROR,
            access_status=AccessStatus.DENIED,
            message=message,
            errors=errors
        )

    @staticmethod
    def paginated(
            items: List[Any],
            total: int,
            page: int,
            size: int,
            message: str = "List retrieved successfully"
    ) -> PaginatedResponse:
        pages = (total + size - 1) // size if size > 0 else 0
        return PaginatedResponse(
            status_code=200,
            status=ResponseStatus.SUCCESS,
            access_status=AccessStatus.GRANTED,
            message=message,
            data={
                "items": items,
                "total": total,
                "page": page,
                "size": size,
                "pages": pages
            }
        )
