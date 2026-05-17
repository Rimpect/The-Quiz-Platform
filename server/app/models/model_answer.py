# ==========  Таблица 5: Ответы ==========
from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .model_media import MediaEntity, MediaType
from ..database.database import Base
from .model_question import Question
from .model_user_answer import UserAnswer


class Answer(Base):
    __tablename__ = "answers"

    # Обязательные поля
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False,
                         index=True)  # ID вопроса
    answer_text = Column(Text, nullable=False)  # Текст ответа
    is_correct = Column(Boolean, default=False, nullable=False)  # Правильный ли ответ

    # Связи
    question = relationship(Question, back_populates="answers")
    user_selected_answers = relationship(UserAnswer, back_populates="selected_answer")

    @property
    def images(self):
        """Изображения ответа"""
        from ..crud import media as media_crud
        from ..database.database import SessionLocal
        db = SessionLocal()
        return media_crud.get_entity_media(
            db, MediaEntity.ANSWER, self.id, MediaType.IMAGE
        )

    def __repr__(self):
        return f"<Answer {self.id}: {self.answer_text[:30]}>"
