"""
Конфигурация Redis
Управление подключением к Redis и ключами
"""
import redis
import os
from dotenv import load_dotenv

load_dotenv()

# Настройки Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

# Создание пула соединений
redis_pool = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    decode_responses=True,  # Автоматически декодировать строки
    max_connections=50
)


def get_redis():
    """Получение соединения с Redis"""
    return redis.Redis(connection_pool=redis_pool)


# Префиксы для ключей (организация данных в Redis)
class RedisKeys:
    """Класс для генерации ключей Redis"""

    # Сессии прохождения квизов
    QUIZ_SESSION = "quiz:session:"  # quiz:session:{session_id}
    USER_ANSWER = "user:answer:"  # user:answer:{session_id}:{question_id}
    SESSION_ANSWERS = "session:answers:"  # session:answers:{session_id}

    # Приватные лобби
    PRIVATE_LOBBY = "lobby:private:"  # lobby:private:{lobby_id}
    USER_LOBBY = "user:lobby:"  # user:lobby:{user_id}

    # Лидерборды
    QUIZ_LEADERBOARD = "quiz:leaderboard:"  # quiz:leaderboard:{quiz_id}

    @staticmethod
    def quiz_session(session_id: str) -> str:
        return f"quiz:session:{session_id}"

    @staticmethod
    def user_answer(session_id: str, question_id: int) -> str:
        return f"user:answer:{session_id}:{question_id}"

    @staticmethod
    def session_answers(session_id: str) -> str:
        return f"session:answers:{session_id}"

    @staticmethod
    def private_lobby(lobby_id: str) -> str:
        return f"lobby:private:{lobby_id}"

    @staticmethod
    def user_lobby(user_id: int) -> str:
        return f"user:lobby:{user_id}"

    @staticmethod
    def quiz_leaderboard(quiz_id: int) -> str:
        return f"quiz:leaderboard:{quiz_id}"


# Время жизни данных (в секундах)
SESSION_TTL = 3600  # 1 час для сессии
ANSWER_TTL = 3600  # 1 час для ответов
LOBBY_TTL = 7200  # 2 часа для лобби
LEADERBOARD_TTL = 86400  # 24 часа для лидерборда
