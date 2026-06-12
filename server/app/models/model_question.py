# ========== Таблица 3: Вопрос ==========
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .model_media import MediaEntity, MediaType
from ..database.database import Base
import enum


class AnswerType(str, enum.Enum):
    SINGLE = "single"  # Одиночный выбор
    MULTIPLE = "multiple"  # Множественный выбор


class Question(Base):
    __tablename__ = "questions"

    # Обязательные поля
    id = Column(Integer, primary_key=True, index=True)
    answer_type = Column(SQLEnum(AnswerType), nullable=False)  # Тип внесения ответа
    points = Column(Integer, default=0, nullable=False)  # Количество баллов
    question_text = Column(Text, nullable=False)  # Содержание вопроса
    question_media_url = Column(String(500), nullable=True)  # Медиа (путь к файлу)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)  # ID квиза
    time_limit_seconds = Column(Integer, nullable=True)  # Время ожидания ответа (в секундах)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # Дата создания
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)  # Дата изменения

    # Связи
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")
    quiz = relationship("Quiz", back_populates="questions")

    @property
    def media_url(self):
        """Алиас для схемы QuestionResponse (поле media_url)"""
        return self.question_media_url

    @property
    def images(self):
        """Изображения вопроса"""
        from ..crud import crud_media as media_crud
        from ..database.database import SessionLocal
        db = SessionLocal()
        return media_crud.get_entity_media(
            db, MediaEntity.QUESTION, self.id, MediaType.IMAGE
        )

    @property
    def audio_files(self):
        """Аудиофайлы вопроса"""
        from ..crud import crud_media as media_crud
        from ..database.database import SessionLocal
        db = SessionLocal()
        return media_crud.get_entity_media(
            db, MediaEntity.QUESTION, self.id, MediaType.AUDIO
        )

    @property
    def video(self):
        """Видеофайлы вопроса"""
        from ..crud import crud_media as media_crud
        from ..database.database import SessionLocal
        db = SessionLocal()
        return media_crud.get_entity_primary_media(
            db, MediaEntity.QUESTION, self.id, MediaType.VIDEO
        )

    def __repr__(self):
        return f"<Question {self.id}: {self.question_text[:50]}>"
