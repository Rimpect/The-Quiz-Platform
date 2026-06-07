"""
Middleware для ограничения частоты запросов (Rate Limiting)
"""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from datetime import datetime, timedelta
import os

# Настройки из .env
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS"))
RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD"))


class RateLimitMiddleware(BaseHTTPMiddleware) :
    """
    Middleware для ограничения количества запросов
    Простая реализация с хранением в памяти
    Для production рекомендуется использовать Redis
    """

    def __init__(self, app) :
        super().__init__(app)
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next) :
        # Получаем IP клиента (учитывая прокси)
        client_ip = request.headers.get("X-Forwarded-For", request.client.host)

        # Очищаем старые записи
        now = datetime.now()
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > now - timedelta(seconds=RATE_LIMIT_PERIOD)
        ]

        # Проверяем лимит
        if len(self.requests[client_ip]) >= RATE_LIMIT_REQUESTS :
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Max {RATE_LIMIT_REQUESTS} requests per {RATE_LIMIT_PERIOD} seconds."
            )

        # Добавляем текущий запрос
        self.requests[client_ip].append(now)

        response = await call_next(request)
        return response