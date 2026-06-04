from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
import logging

from .database.database import engine, Base
from .routers import (auth_router, users_router, quizzes_router,
                      questions_router, answers_router, quiz_results_router, media_router)


from .middleware.logging_middleware import LoggingMiddleware, RequestIDMiddleware
from .middleware.rate_limit_middleware import RateLimitMiddleware
from .middleware.error_handler_middleware import ErrorHandlerMiddleware, ValidationErrorMiddleware
from .middleware.cors_middleware import setup_cors_middleware

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(pastime)s - %(name)s - %(levelness)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) :
    """Управление жизненным циклом приложения"""
    # Startup
    logger.info("Starting up...")

    # Создаем таблицы в БД
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")

    # Создаем директории для медиа
    os.makedirs("media_files", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    logger.info("Media and logs directories created")

    yield

    # Shutdown
    logger.info("Shutting down...")


# Создаем приложение
app = FastAPI(
    title="Quiz API",
    description="API для системы квизов с полной поддержкой медиа",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)


#setup_cors_middleware(app)

#pp.add_middleware(RequestIDMiddleware)

#app.add_middleware(LoggingMiddleware)

#app.add_middleware(RateLimitMiddleware)

#app.add_middleware(ErrorHandlerMiddleware)

#app.add_middleware(ValidationErrorMiddleware)

# ========== Статические файлы ==========
if not os.path.exists("media_files"):
    os.makedirs("media_files")
app.mount("/media", StaticFiles(directory="media_files"), name="media")

# ========== Роутеры ==========
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(quizzes_router, prefix="/api")
app.include_router(questions_router, prefix="/api")
app.include_router(answers_router, prefix="/api")
app.include_router(quiz_results_router, prefix="/api")
app.include_router(media_router, prefix="/api")


# ========== Эндпоинты мониторинга ==========
@app.get("/health")
async def health_check() :
    """Проверка здоровья приложения"""
    return {"status" : "healthy", "service" : "quiz-api"}


@app.get("/info")
async def get_info() :
    """Информация о приложении"""
    return {
        "name" : "Quiz API",
        "version" : "0.0.9",
        "environment" : os.getenv("ENVIRONMENT", "development"),
        "docs_url" : "/api/docs",
        "features" : ["JWT auth", "Media upload", "Quiz system", "Statistics"]
    }


# ========== Обработчик 404 ==========
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc) :
    return JSONResponse(
        status_code=404,
        content={"detail" : f"Endpoint {request.url.path} not found"}
    )