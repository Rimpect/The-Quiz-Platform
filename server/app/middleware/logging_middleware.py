import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware) :
    """Middleware для логирования всех запросов"""

    async def dispatch(self, request: Request, call_next) :
        # Начало обработки запроса
        start_time = time.time()

        # Логируем входящий запрос
        logger.info(f"Incoming request: {request.method} {request.url.path}")

        # Логируем заголовки (опционально)
        # logger.debug(f"Headers: {dict(request.headers)}")

        # Логируем параметры запроса
        if request.query_params :
            logger.debug(f"Query params: {dict(request.query_params)}")

        # Обрабатываем запрос
        response = await call_next(request)

        # Вычисляем время выполнения
        process_time = time.time() - start_time

        # Логируем ответ
        logger.info(
            f"Response: {request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.3f}s"
        )

        # Добавляем заголовок с временем выполнения
        response.headers["X-Process-Time"] = str(process_time)

        return response


class RequestIDMiddleware(BaseHTTPMiddleware) :
    """Middleware для добавления уникального ID запроса"""

    async def dispatch(self, request: Request, call_next) :
        import uuid

        # Генерируем уникальный ID для запроса
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id

        # Добавляем в логи
        logger.debug(f"Request ID: {request_id}")

        response = await call_next(request)

        # Добавляем в заголовок ответа
        response.headers["X-Request-ID"] = request_id

        return response