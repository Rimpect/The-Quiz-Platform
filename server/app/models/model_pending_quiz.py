import enum

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database.database import Base


class PendingQuizStatus(str, enum.Enum) :
    PENDING = "pending"  # На модерации
    APPROVED = "approved"  # Одобрен
    REJECTED = "rejected"  # Отклонён


class PendingQuiz(Base) :
    """Таблица квизов на модерации"""
    __tablename__ = "pending_quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    description = Column(Text, nullable=False)
    cover_url = Column(String(500), nullable=True)
    quiz_mode = Column(String(20), default="single", nullable=False)

    # Статус модерации
    status = Column(SQLEnum(PendingQuizStatus), default=PendingQuizStatus.PENDING, nullable=False)

    # Кто создал
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    moderated_at = Column(DateTime(timezone=True), nullable=True)
    moderated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Связи
    author = relationship("User", foreign_keys=[author_id], backref="pending_quizzes")
    moderator = relationship("User", foreign_keys=[moderated_by])
    category = relationship("Category")

    def __repr__(self) :
        return f"<PendingQuiz {self.title} (status={self.status})>"