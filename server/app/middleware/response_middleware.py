"""
Middleware для форматирования всех ответов в единый шаблон
"""
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import json
from datetime import datetime


class ResponseFormatterMiddleware(BaseHTTPMiddleware) :
    """
    Middleware для форматирования всех ответов в единый шаблон

    Формат ответа:
    {
        "status_code": 200,
        "status": "success",
        "access_status": "granted",
        "message": "Operation successful",
        "timestamp": "2024-01-01T12:00:00",
        "data": {...},
        "errors": null
    }
    """

    async def dispatch(self, request: Request, call_next) :
        # Обрабатываем запрос
        response = await call_next(request)

        # Пропускаем статические файлы
        if request.url.path.startswith("/media") or request.url.path.startswith("/static") :
            return response

        # Пропускаем не JSON ответы
        if response.headers.get("content-type") != "application/json" :
            return response

        # Получаем тело ответа
        body = b""
        async for chunk in response.body_iterator :
            body += chunk

        try :
            response_data = json.loads(body.decode())
        except :
            return response

        # Если ответ уже отформатирован - пропускаем
        if isinstance(response_data, dict) and "status_code" in response_data :
            return JSONResponse(
                status_code=response_data.get("status_code", response.status_code),
                content=response_data
            )

        # Определяем статус доступа из заголовка (если есть)
        access_status = request.headers.get("X-Access-Status", "granted")

        # Форматируем ответ в зависимости от HTTP статуса
        if 200 <= response.status_code < 300 :
            formatted = {
                "status_code" : response.status_code,
                "status" : "success" if response.status_code == 200 else "created",
                "access_status" : access_status,
                "message" : response_data.get("message", "Operation successful") if isinstance(response_data,
                                                                                               dict) else "Operation successful",
                "timestamp" : datetime.utcnow().isoformat(),
                "data" : response_data if response_data else None,
                "errors" : None
            }
        elif response.status_code == 400 :
            formatted = {
                "status_code" : 400,
                "status" : "bad_request",
                "access_status" : "denied",
                "message" : response_data.get("detail", "Bad request") if isinstance(response_data,
                                                                                     dict) else "Bad request",
                "timestamp" : datetime.utcnow().isoformat(),
                "data" : None,
                "errors" : response_data.get("errors") if isinstance(response_data, dict) else None
            }
        elif response.status_code == 401 :
            formatted = {
                "status_code" : 401,
                "status" : "unauthorized",
                "access_status" : "missing",
                "message" : response_data.get("detail", "Authentication required") if isinstance(response_data,
                                                                                                 dict) else "Authentication required",
                "timestamp" : datetime.utcnow().isoformat(),
                "data" : None,
                "errors" : None
            }
        elif response.status_code == 403 :
            formatted = {
                "status_code" : 403,
                "status" : "forbidden",
                "access_status" : "denied",
                "message" : response_data.get("detail", "Access forbidden") if isinstance(response_data,
                                                                                          dict) else "Access forbidden",
                "timestamp" : datetime.utcnow().isoformat(),
                "data" : None,
                "errors" : None
            }
        elif response.status_code == 404 :
            formatted = {
                "status_code" : 404,
                "status" : "not_found",
                "access_status" : "granted",
                "message" : response_data.get("detail", "Resource not found") if isinstance(response_data,
                                                                                            dict) else "Resource not found",
                "timestamp" : datetime.utcnow().isoformat(),
                "data" : None,
                "errors" : None
            }
        else :
            formatted = {
                "status_code" : response.status_code,
                "status" : "error",
                "access_status" : "denied",
                "message" : response_data.get("detail", "Internal server error") if isinstance(response_data,
                                                                                               dict) else "Internal server error",
                "timestamp" : datetime.utcnow().isoformat(),
                "data" : None,
                "errors" : response_data.get("errors") if isinstance(response_data, dict) else None
            }

        return JSONResponse(
            status_code=formatted["status_code"],
            content=formatted
        )
