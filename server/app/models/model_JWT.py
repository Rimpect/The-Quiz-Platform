# ========== Таблица 6: JWT-токены ==========
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base
import enum


"""

"""


class JWT_token(Base):
    __tablename__ = "jwt_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Хеш refresh токена (никогда не храним сам токен в открытом виде!)
    refresh_token_hash = Column(String(255), nullable=False, unique=True, index=True)

    # Метаданные токена
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_login = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Связь с пользователем
    user = relationship("User", back_populates="jwt_tokens")

    def __repr__(self) :
        return f"<JWT_token {self.id}: user_id={self.user_id}, expires={self.expires_at}>"

    @property
    def is_revoked(self) -> bool :
        """Проверка, отозван ли токен"""
        return self.revoked_at is not None

    @property
    def is_expired(self) -> bool :
        """Проверка, истек ли токен"""
        from datetime import datetime
        return datetime.now(self.expires_at.tzinfo) > self.expires_at if self.expires_at else True

    @property
    def is_valid(self) -> bool :
        """Проверка, действителен ли токен"""
        return not self.is_revoked and not self.is_expired