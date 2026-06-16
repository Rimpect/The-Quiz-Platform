"""
Главный файл приложения FastAPI
Содержит настройки CORS, middleware, lifespan, роутеры
"""
import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Redis (опционально)
try:
    from .config_redis.redis_config import get_redis, redis_pool
    from .config_redis.redis_service import cleanup_expired_sessions
    REDIS_AVAILABLE = True
except ImportError:
    redis_pool = None
    get_redis = None
    cleanup_expired_sessions = None
    REDIS_AVAILABLE = False
# CRUD
from .crud.crud_guest import Guest as guest_crud
# База данных
from .database.database import engine, Base, close_db_connections, get_db, test_connection
# Middleware
from .middleware.error_handler_middleware import ErrorHandlerMiddleware
from .middleware.logging_middleware import LoggingMiddleware
from .middleware.rate_limit_middleware import RateLimitMiddleware
from .middleware.response_middleware import ResponseFormatterMiddleware
from .utils.logger import get_logger
# Модели (для автоматического создания таблиц)
from .models import (
    User, Quiz, Question, Answer, Category, UserAchievement,
    QuizResult, UserAnswer, MediaEntity, Guest, PendingQuiz,
    GameSession, TeamMember, JWTToken
)

# Роутеры
from .routers import (
    achievements_router,
    admin_router,
    auth_router,
    game_router,
    users_router,
    guest_router,
    quizzes_router,
    categories_router,
    questions_router,
    answers_router,
    quiz_results_router,
    quiz_session_router,
    lobby_router,
    media_router
)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = get_logger(__name__)


# ========== LIFESPAN (управление жизненным циклом) ==========
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("STARTING UP APPLICATION")

    # 1. Создаём таблицы в отдельном потоке, чтобы не блокировать event-loop
    logger.info("Creating database tables...")
    await asyncio.to_thread(Base.metadata.create_all, bind=engine)
    logger.info("Database tables created")

    # Авто-миграция: добавляем недостающие колонки моделей (create_all не делает ALTER)
    def _sync_columns():
        from .database.auto_migrate import sync_missing_columns
        return sync_missing_columns(engine)

    try:
        added_cols = await asyncio.to_thread(_sync_columns)
        if added_cols:
            logger.info(f"Auto-migrate: {added_cols} column(s) added")
    except Exception as e:
        logger.error(f"Auto-migrate failed: {e}")

    def _seed_categories():
        from .crud import crud_categories
        from .database.database import SessionLocal
        db = SessionLocal()
        try:
            return crud_categories.seed_default_categories(db)
        finally:
            db.close()

    try:
        added = await asyncio.to_thread(_seed_categories)
        logger.info(f"Default categories seeded (added: {added})")
    except Exception as e:
        logger.error(f"Category seeding failed: {e}")

    # Структура папок для медиа (media/...)
    from .utils.media_utils import ensure_media_dirs
    ensure_media_dirs()
    logger.info("Media directories ensured")

    # 2. Проверяем подключение, также в отдельном потоке, с таймаутом
    try:
        # asyncio.to_thread позволяет выполнить синхронную функцию test_connection в потоке
        is_connected = await asyncio.wait_for(
            asyncio.to_thread(test_connection),
            timeout=10.0 # Таймаут в 10 секунд
        )
        if is_connected:
            logger.info("PostgresSQL connection established")
        else:
            logger.warning("PostgresSQL connection check returned False")
    except asyncio.TimeoutError:
        logger.error("PostgresSQL connection timed out after 10 seconds")
    except Exception as e:
        logger.error(f"PostgresSQL connection failed: {e}")

    # 3. Проверка подключения к Redis (если доступен)
    if REDIS_AVAILABLE and get_redis:
        try:
            # Таймаут 5 секунд на подключение к Redis
            redis_client = await asyncio.wait_for(
                asyncio.to_thread(get_redis),
                timeout=5.0
            )
            redis_client.ping()
            logger.info("Redis connection established")
        except asyncio.TimeoutError:
            logger.warning("Redis connection timeout - continuing without Redis")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}")
    else:
        logger.warning("Redis not available - continuing without Redis")

    # 4. Создание директорий
    os.makedirs("media_files", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    logger.info("Media and logs directories created")

    # 5. Фоновая задача для очистки устаревших данных
    async def background_cleanup():
        """Периодическая очистка устаревших данных"""
        while True:
            await asyncio.sleep(3600)  # Каждый час
            try:
                # Очистка истекших гостей
                db = next(get_db())
                try:
                    deleted_guests = guest_crud.delete_expired_guests(db)
                    if deleted_guests:
                        logger.info(f"Cleaned up {deleted_guests} expired guests")
                finally:
                    db.close()

                # Очистка истекших сессий в Redis
                deleted_redis = cleanup_expired_sessions()
                if deleted_redis:
                    logger.info(f"Cleaned up {deleted_redis} expired Redis sessions")

            except Exception as exc:
                logger.error(f"Background cleanup error: {exc}")

    # Фоновый тикер WebSocket командных игр (пуш состояния вместо поллинга)
    from .services.ws_manager import game_ws_ticker
    asyncio.create_task(game_ws_ticker())
    logger.info("Game WebSocket ticker started")

    # Запуск фоновой задачи очистки (без await — не блокировать старт)
    asyncio.create_task(background_cleanup())
    logger.info("Background cleanup task started")

    logger.info("=" * 50)
    logger.info("APPLICATION STARTED SUCCESSFULLY")
    logger.info("=" * 50)

    yield  # Приложение работает

    # ========== SHUTDOWN ==========
    logger.info("=" * 50)
    logger.info("SHUTTING DOWN APPLICATION")
    logger.info("=" * 50)

    try:
        # 1. Закрытие PostgreSQL соединений
        close_db_connections()
        logger.info("PostgreSQL connections closed")

        # 2. Закрытие Redis соединений (если доступен)
        if REDIS_AVAILABLE and redis_pool:
            redis_pool.disconnect()
            logger.info("Redis connections closed")

    except Exception as e:
        logger.error(f"Shutdown error: {e}")

    logger.info("Application shutdown complete")
    logger.info("=" * 50)


# ========== СОЗДАНИЕ ПРИЛОЖЕНИЯ ==========
app = FastAPI(
    title="Quiz API",
    description="API для системы квизов с поддержкой Redis, гостей и приватных лобби",
    version="3.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    openapi_version="3.1.0",
    redirect_slashes=False,
)

from .services.exception_handlers import register_exception_handlers
register_exception_handlers(app)


app.add_middleware(ResponseFormatterMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(ErrorHandlerMiddleware)

# CORS — последний = самый внешний, добавляет заголовки поверх всех остальных middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "Accept",
        "Origin",
        "X-Requested-With"
    ],
    expose_headers=["X-Request-ID", "X-Process-Time"],
    max_age=3600,
)
#
# # ========== СТАТИЧЕСКИЕ ФАЙЛЫ ==========
# app.mount("/media", StaticFiles(directory="media_files"), name="media")

# ========== ПОДКЛЮЧЕНИЕ РОУТЕРОВ ==========
app.include_router(achievements_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(game_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(guest_router, prefix="/api")
app.include_router(quizzes_router, prefix="/api")
app.include_router(categories_router, prefix="/api")
app.include_router(questions_router, prefix="/api")
app.include_router(answers_router, prefix="/api")
app.include_router(quiz_results_router, prefix="/api")
app.include_router(quiz_session_router, prefix="/api")
app.include_router(lobby_router, prefix="/api")
app.include_router(media_router, prefix="/api")
app.include_router(admin_router, prefix="/api")

# ========== СИСТЕМНЫЕ ЭНДПОИНТЫ ==========
@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "name": "Quiz API",
        "version": "3.0.0",
        "status": "running",
        "docs": "/api/docs",
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья всех компонентов"""
    health = {
        "status": "healthy",
        "components": {}
    }

    # Проверка PostgreSQL
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        health["components"]["postgresql"] = "healthy"
    except Exception as e:
        health["components"]["postgresql"] = f"unhealthy: {str(e)}"
        health["status"] = "unhealthy"

    # Проверка Redis
    try:
        redis_client = get_redis()
        redis_client.ping()
        health["components"]["redis"] = "healthy"
    except Exception as e:
        health["components"]["redis"] = f"unhealthy: {str(e)}"
        health["status"] = "unhealthy"

    return health


@app.get("/info")
async def get_info():
    """Информация о приложении"""
    return {
        "name": "Quiz API",
        "version": "3.0.0",
        "features": [
            "JWT authentication",
            "Guest users",
            "Redis sessions for quiz taking",
            "Private lobbies",
            "Real-time leaderboards",
            "Media upload",
            "Bulk quiz creation",
            "Categories reference"
        ]
    }


# ========== ЗАПУСК (для прямого выполнения) ==========
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        timeout_graceful_shutdown=30,
        lifespan="on"
    )