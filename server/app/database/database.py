from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("DB_USER")
POSTGRES_PASSWORD = os.getenv("DB_PASSWORD")
POSTGRES_HOST = os.getenv("DB_HOST")
POSTGRES_PORT = os.getenv("DB_PORT")
POSTGRES_DB = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Настройка engine с пулом соединений
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,      # Проверка соединения перед использованием
    pool_recycle=3600,       # Переподключение через час
    pool_size=10,            # Размер пула
    max_overflow=20,         # Максимальное дополнительных соединений
    echo=False               # SQL логирование (True для отладки)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Генератор сессий базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def close_db_connections():
    """
    Закрытие всех соединений с БД
    Вызывается при завершении работы приложения
    """
    engine.dispose()
    print("Database connections closed")


def test_connection():
    """Тест подключения к БД"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database connection successful")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False
