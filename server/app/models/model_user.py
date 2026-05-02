# ========== Таблица 1: Пользователь ==========
from sqlalchemy import (Column, Integer, String, DateTime, Enum as SQLEnum)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base
import enum
from model_JWT import JWTToken
from model_statistic import QuizResult


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    AUTHOR = "author"


class ThemeMode(str, enum.Enum):
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


class User(Base):
    __tablename__ = "users"

    # Обязательные поля
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50), nullable=False)  # Никнейм
    theme_site = Column(SQLEnum(ThemeMode), default=ThemeMode.LIGHT, nullable=False)  # Тема сайта
    photo_profile = Column(String(500), nullable=True)  # Фото профиля (путь к файлу)
    login = Column(String(50), unique=True, nullable=False, index=True)  # Логин
    email = Column(String(100), unique=True, nullable=False, index=True)  # Почта
    password_hash = Column(String(255), nullable=False)  # Пароль (хеш)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # Дата регистрации
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)  # Дата изменения

    # Связи
    refresh_tokens = relationship(JWTToken, back_populates="user", cascade="all, delete-orphan")
    quiz_results = relationship(QuizResult, back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) :
        return f"<User {self.login}>"
