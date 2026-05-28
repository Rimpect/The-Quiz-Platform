# ========== Таблица 1: Пользователь ==========
import enum
from typing import Optional

from sqlalchemy import (Column, Integer, String, DateTime, Enum as SQLEnum)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .model_media import MediaEntity, MediaType
from ..database.database import Base


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
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)  # Дата изменения
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)

    # Связи
    jwt_tokens = relationship("JWTToken", back_populates="user", cascade="all, delete-orphan")
    quiz_results = relationship("QuizResult", back_populates="user", cascade="all, delete-orphan")
    quiz = relationship("Quiz", back_populates="user_author", cascade="all, delete-orphan")

    @property
    def profile_images(self) :
        """Получение всех изображений профиля пользователя"""
        from ..crud import media as media_crud
        from ..database.database import SessionLocal
        db = SessionLocal()
        return media_crud.get_entity_media(
            db, MediaEntity.PROFILE, self.id, MediaType.IMAGE
        )

    @property
    def profile_image_url(self) -> Optional[str]:
        """URL основного изображения профиля"""
        from ..crud import media as media_crud
        from ..database.database import SessionLocal
        db = SessionLocal()
        media = media_crud.get_entity_primary_media(
            db, MediaEntity.PROFILE, self.id, MediaType.IMAGE
        )
        return media.url if media else None

    def __repr__(self) :
        return f"<User {self.login}>"
