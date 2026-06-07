"""
Временная таблица для хранения ответов пользователей во время прохождения квиза
Данные хранятся в Redis, модель только для SQLAlchemy (опционально для бэкапа)
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base


class UserAnswer(Base):
    """
    Модель для бэкапа ответов в PostgreSQL (опционально)
    Основное хранение - в Redis
    """
    __tablename__ = "user_answers_backup"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    guest_id = Column(Integer, nullable=True)  # Для гостей
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)

    # Ответ пользователя
    answer_text = Column(Text, nullable=True)
    answer_ids = Column(String(500), nullable=True)  # JSON строка для множественного выбора
    is_correct = Column(Boolean, default=False)
    points_earned = Column(Integer, default=0)
    time_spent_seconds = Column(Integer, default=0)
    question_order = Column(Integer, default=0)

    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Связи
    quiz = relationship("Quiz", foreign_keys=[quiz_id])
    question = relationship("Question", foreign_keys=[question_id])

    def __repr__(self):
        return f"<UserAnswer session={self.session_id}, q={self.question_id}>"
