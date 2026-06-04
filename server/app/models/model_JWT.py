# ========== Таблица: JWT-токены (Access + Refresh) ==========
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from ..database.database import Base


class JWTToken(Base):
    """
    Таблица для хранения JWT токенов

    Особенности:
    - Хранение хэш токенов
    - Поддерживается отзыв (revoke) отдельных токенов
    """
    __tablename__ = "jwt_tokens"

    # ========== Обязательные поля ==========
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)

    # Хеши токенов (никогда не храним сами токены!)
    access_token_hash = Column(String(255), nullable=False, index=True)  # Хеш access токена
    refresh_token_hash = Column(String(255), nullable=False, unique=True, index=True)  # Хеш refresh токена

    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # ========== Управление жизненным циклом ==========
    access_expires_at = Column(DateTime(timezone=True), nullable=False)  # Когда истекает access токен
    refresh_expires_at = Column(DateTime(timezone=True), nullable=False)  # Когда истекает refresh токен

    # Статус токена
    is_access_revoked = Column(Boolean, default=False, nullable=False)  # Отозван ли access токен
    is_refresh_revoked = Column(Boolean, default=False, nullable=False)  # Отозван ли refresh токен
    revoked_at = Column(DateTime(timezone=True), nullable=True)  # Дата отзыва (общая для пары)
    revoked_reason = Column(String(200), nullable=True)  # Причина отзыва

    # ========== Метаданные для безопасности ==========
    user_agent = Column(String(500), nullable=True)  # Информация об устройстве/браузере
    #ip_address = Column(String(45), nullable=True)  # IP адрес (поддерживает IPv6)
    last_used_at = Column(DateTime(timezone=True), nullable=True)  # Время последнего использования

    # ========== Связи ==========
    user = relationship("User", back_populates="jwt_tokens")

    def __repr__(self) :
        return f"<JWTToken id={self.id}, user_id={self.user_id}>"

    # ========== Свойства для удобства ==========
    @property
    def is_access_valid(self) -> bool :
        """Проверка, действителен ли access токен"""
        now = datetime.now(self.access_expires_at.tzinfo) if self.access_expires_at else datetime.utcnow()
        return (
                not self.is_access_revoked and
                self.access_expires_at and
                now < self.access_expires_at
        )

    @property
    def is_refresh_valid(self) -> bool :
        """Проверка, действителен ли refresh токен"""
        now = datetime.now(self.refresh_expires_at.tzinfo) if self.refresh_expires_at else datetime.utcnow()
        return (
                not self.is_refresh_revoked and
                self.refresh_expires_at and
                now < self.refresh_expires_at
        )

    @property
    def is_fully_valid(self) -> bool :
        """Проверка, действительны ли оба токена"""
        return self.is_access_valid and self.is_refresh_valid

    @property
    def is_fully_revoked(self) -> bool :
        """Проверка, отозваны ли оба токена"""
        return self.is_access_revoked and self.is_refresh_revoked

    def revoke_access(self, reason: str = "Revoked") -> None :
        """Отзыв access токена"""
        self.is_access_revoked = True
        self.revoked_at = datetime.utcnow()
        self.revoked_reason = reason

    def revoke_refresh(self, reason: str = "Revoked") -> None :
        """Отзыв refresh токена"""
        self.is_refresh_revoked = True
        self.revoked_at = datetime.utcnow()
        self.revoked_reason = reason

    def revoke_both(self, reason: str = "Both tokens revoked") -> None :
        """Отзыв обоих токенов"""
        self.is_access_revoked = True
        self.is_refresh_revoked = True
        self.revoked_at = datetime.utcnow()
        self.revoked_reason: str = reason

    def update_last_used(self) -> None :
        """Обновление времени последнего использования"""
        self.last_used_at = datetime.utcnow()
