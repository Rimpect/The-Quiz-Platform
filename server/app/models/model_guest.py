# ========== Временная таблица: Гости ==========
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..database.database import Base


class Guest(Base) :
    """
    Временная таблица для гостевых пользователей
    Данные автоматически удаляются после истечения срока
    """
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50), nullable=False, index=True)
    session_id = Column(String(100), unique=True, nullable=False, index=True)  # Уникальный ID сессии


    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)  # Время истечения
    last_active_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self) :
        return f"<Guest {self.nickname} (expires: {self.expires_at})>"
