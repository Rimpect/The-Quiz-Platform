# ========== Таблица 4: Статистика прохождения (Результаты) ==========
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base
from model_user import User
from model_quiz import Quiz
from model_user_answer import UserAnswer




class QuizResult(Base):
    __tablename__ = "quiz_results"

    # Сохраняемые поля
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)  # ID пользователя
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)  # ID квиза
    score = Column(Float, nullable=False)  # Полученные баллы
    is_completed = Column(Boolean, default=False, nullable=False)  # Пройден ли полностью
    max_score = Column(Float, nullable=False)  # Максимально возможные баллы
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # Дата старта
    completed_at = Column(DateTime(timezone=True), nullable=True)  # Дата прохождения

    # Вычисляемое поле
    # duration_seconds - вычисляется как разница между completed_at и started_at

    # Связи
    user = relationship(User, back_populates="quiz_results")
    quiz = relationship(Quiz, back_populates="results")
    user_answers = relationship(UserAnswer, back_populates="quiz_result", cascade="all, delete-orphan")

    # Вычисляемые свойства
    @property
    def duration_seconds(self) -> int :
        """Время прохождения в секундах (вычисляемое)"""
        if self.completed_at and self.started_at :
            delta = self.completed_at - self.started_at
            return int(delta.total_seconds())
        return 0

    @property
    def percentage(self) -> float :
        """Процент правильных ответов"""
        if self.max_score > 0 :
            return (self.score / self.max_score) * 100
        return 0.0

    def __repr__(self) :
        return f"<QuizResult user={self.user_id}, quiz={self.quiz_id}, score={self.score}>"
