# ==========  Таблица 5: Ответы ==========
from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey, func, DateTime
from sqlalchemy.orm import relationship
from ..database.database import Base


class Answer(Base):
    __tablename__ = "answers"

    # Обязательные поля
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False,
                         index=True)  # ID вопроса
    answer_text = Column(Text, nullable=False)  # Текст ответа
    is_correct = Column(Boolean, default=False, nullable=False)  # Правильный ли ответ
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # Дата создания
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),onupdate=func.now(), nullable=False)  # Дата изменения

    # Связи
    question = relationship("Question", back_populates="answers")

    def __repr__(self):
        return f"<Answer {self.id}: {self.answer_text[:30]}>"
