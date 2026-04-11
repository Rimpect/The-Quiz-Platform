# ==========  Таблица 5: Ответы ==========
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base
import enum

class Answer(Base):
    __tablename__ = "answer_options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)

    option_text = Column(Text, nullable=False)  # Текст варианта ответа
    is_correct = Column(Boolean, default=False)  # Является ли этот вариант правильным
    order_number = Column(Integer, default=0)  # Порядок отображения

    # Связи
    question = relationship("Question", back_populates="answer_options")

    def __repr__(self) :
        return f"<AnswerOption {self.id}: {self.option_text[:30]}>"
