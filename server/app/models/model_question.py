# ========== Таблица 3: Вопрос ==========
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base
import enum

class AnswerType(str, enum.Enum) :
    SINGLE = "single"  # Одиночный выбор
    MULTIPLE = "multiple"  # Множественный выбор
    TEXT = "text"  # Текстовый ответ
    NUMERIC = "numeric"  # Числовой ответ




class Question(Base) :
    __tablename__ = "questions"

    # Основные поля
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    order_number = Column(Integer, nullable=False)  # Порядковый номер вопроса в квизе

    # Содержание вопроса
    question_text = Column(Text, nullable=False)  # Текст вопроса
    content = Column(Text, nullable=True)  # Дополнительное содержание
    media_url = Column(String(500), nullable=True)  # Медиа (изображение, видео и т.д.)

    # Настройки ответа
    answer_type = Column(SQLEnum(AnswerType), default=AnswerType.SINGLE)
    points = Column(Integer, default=1)  # Баллы за правильный ответ

    # Варианты ответов (хранятся в отдельной таблице для гибкости)
    # Правильный ответ может быть текстовым или ссылкой на варианты

    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    quiz = relationship("Quiz", back_populates="questions")
    answer_options = relationship("Answer", back_populates="question", cascade="all, delete-orphan")


    def __repr__(self) :
        return f"<Question {self.id}: {self.question_text[:50]}>"