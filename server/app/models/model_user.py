# ========== Таблица 1: Пользователь ==========
from sqlalchemy import (Column, Integer, String, DateTime, Enum as SQLEnum)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base
import enum


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

    # Основные поля
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(50), unique=True, nullable=False, index=True)  # Логин пользователя-текст до 50, обяз, индекс.
    email = Column(String(100), unique=True, nullable=False,
                   index=True)  # Почта пользователя-текст до 100, обяз, индекс.
    password_hash = Column(String(255), nullable=False)  # Хэш-пароль пользователя-текст до 255, обяз.

    # Публичная информация
    nickname = Column(String(50), nullable=True)  # Имя для других-текст до 50, не обяз.
    avatar_url = Column(String(50), nullable=True)  # Путь к фото профиля-текст до 50, не обяз.

    # Настройки
    role = Column(SQLEnum(UserRole), default=UserRole.USER,
                  nullable=False)  # Роль-словарь, пользователь по умолч, обяз.
    theme_site = Column(SQLEnum(ThemeMode), default=ThemeMode.LIGHT,
                        nullable=False)  # тема-словарь, светлая по умолч, обяз.

    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи с другими таблицами
    quiz_results = relationship("QuizResult", back_populates="user", cascade="all, delete-orphan")
    jwt_tokens = relationship("JWT_token", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) :
        return f"<User {self.login}>"
