# ========== Таблица 6: JWT-токены ==========
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base
import enum


"""

"""


class JWTToken(Base) :
    __tablename__ = "jwt_tokens"

    # Обязательные поля
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)  # ID пользователя
    refresh_token_hash = Column(String(255), nullable=False, unique=True)  # Refresh токен (хеш)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # Дата создания

    # Дополнительные поля для безопасности
    expires_at = Column(DateTime(timezone=True), nullable=False)  # Дата истечения
    revoked_at = Column(DateTime(timezone=True), nullable=True)  # Дата отзыва
    #user_agent = Column(String(500), nullable=True)  # Информация об устройстве
    
    # Связи
    user = relationship("User", back_populates="jwt_tokens")

    def __repr__(self) :
        return f"<JWTToken user_id={self.user_id}>"