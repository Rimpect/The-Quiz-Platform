# ========== Таблица 4: Статистика прохождения (Результаты) ==========
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base
import enum




class QuizResult(Base) :
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)

    # Результаты
    score = Column(Float, nullable=False)  # Набранные баллы
    max_score = Column(Float, nullable=False)  # Максимально возможные баллы
    # Процент выполнения (score/max_score * 100)

    # Временные метки
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)  # Дата прохождения
    duration_seconds = Column(Integer, nullable=True)  # Время прохождения в секундах

    # Статус
    is_completed = Column(Boolean, default=False)

    # Связи
    user = relationship("User", back_populates="quiz_results")
    quiz = relationship("Quiz", back_populates="results")
    answers = relationship("UserAnswer", back_populates="quiz_result", cascade="all, delete-orphan")

    def __repr__(self) :
        return f"<QuizResult {self.user_id}:{self.quiz_id} - {self.percentage}%>"
