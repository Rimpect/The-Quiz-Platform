"""Доменные исключения сервисного слоя.

Сервисы их кидают, не зная про HTTP. Маппинг в HTTP-ответы — в
exception_handlers.register_exception_handlers (см. main.py).
"""


class ServiceError(Exception):
    status_code = 500

    def __init__(self, message: str = "", *, errors=None):
        self.message = message
        self.errors = errors
        super().__init__(message)


class BadRequestError(ServiceError):
    status_code = 400


class UnauthorizedError(ServiceError):
    status_code = 401


class ForbiddenError(ServiceError):
    status_code = 403


class NotFoundError(ServiceError):
    status_code = 404


class ConflictError(ServiceError):
    status_code = 409
