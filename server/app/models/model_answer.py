# ==========  Таблица 5: Ответы ==========
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base
from .model_question import Question

class Answer(Base) :
    __tablename__ = "answers"

    # Обязательные поля
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False,
                         index=True)  # ID вопроса
    answer_text = Column(Text, nullable=False)  # Текст ответа
    is_correct = Column(Boolean, default=False, nullable=False)  # Правильный ли ответ

    # Связи
    question = relationship(Question, back_populates="answers")
    user_selected_answers = relationship("UserAnswer", back_populates="selected_answer")

    def __repr__(self) :
        return f"<Answer {self.id}: {self.answer_text[:30]}>"