from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..database.database import Base


class Guest(Base):
    """Временная таблица для гостевых пользователей"""
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50), nullable=False)  # Автоматически генерируется
    session_id = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    last_active_at = Column(DateTime(timezone=True), onupdate=func.now())
