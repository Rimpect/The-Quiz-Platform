# ========== Таблица 3: Вопрос ==========
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base
import enum
from .model_quiz import Quiz



class AnswerType(str, enum.Enum) :
    SINGLE = "single"  # Одиночный выбор
    MULTIPLE = "multiple"  # Множественный выбор
    TEXT = "text"  # Текстовый ответ
    NUMERIC = "numeric"  # Числовой ответ




class Question(Base) :
    __tablename__ = "questions"

    # Обязательные поля
    id = Column(Integer, primary_key=True, index=True)
    answer_type = Column(SQLEnum(AnswerType), nullable=False)  # Тип внесения ответа
    points = Column(Integer, default=1, nullable=False)  # Количество баллов
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # Дата создания
    question_text = Column(Text, nullable=False)  # Содержание вопроса
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)  # Дата изменения
    media_url = Column(String(500), nullable=True)  # Медиа (путь к файлу)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)  # ID квиза
    time_limit_seconds = Column(Integer, nullable=True)  # Время ожидания ответа (в секундах)

    # Связи
    quiz = relationship("Quiz", back_populates="questions")
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")
    user_answers = relationship("UserAnswer", back_populates="question", cascade="all, delete-orphan")

    def __repr__(self) :
        return f"<Question {self.id}: {self.question_text[:50]}>"