# ========== Таблица 2: Квиз ==========
import enum
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .model_media import MediaEntity, MediaType
from ..database.database import Base


class QuizMode(str, enum.Enum):
    SINGLE = "single"  # Одиночный режим
    TEAM = "team"  # Командный режим
    COMPETITIVE = "competitive"  # соревновательный


class Quiz(Base):
    __tablename__ = "quizzes"

    # Обязательные поля
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)  # Название
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)  # Ссылка на категории
    description = Column(Text, nullable=True)  # Описание
    is_public = Column(Boolean, default=True, nullable=False)  # Публичность квиза
    quiz_mode = Column(SQLEnum(QuizMode), default=QuizMode.SINGLE, nullable=False)  # Режим команды
    author = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # Дата создания
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)  # Дата изменения
    quiz_photo_url = Column(String(500), nullable=True)  # Обложка (путь к файлу)
    description_photo_url = Column(String(500), nullable=True)  # Картинка карточки (путь к файлу)

    # Вычисляемые поля без сохранения 
    # duration_minutes - вычисляется из вопросов
    # total_questions - вычисляется из вопросов
    # difficulty - вычисляется на основе вопросов
    # times_taken - вычисляется из статистики прохождений

    # Связи
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    quiz_results = relationship("QuizResult", back_populates="quiz", cascade="all, delete-orphan")
    user_author = relationship("User", back_populates="quiz", cascade="all, delete-orphan")
    category_ref = relationship("Category", back_populates="quizzes")

    # Вычисляемые свойства (property)
    @property
    def total_questions(self) -> int:
        """Количество вопросов в квизе"""
        return len(self.questions) if self.questions else 0

    @property
    def duration_minutes(self) -> int:
        """Длительность квиза в минутах (сумма времени ожидания ответа на все вопросы)"""
        if not self.questions:
            return 0
        total_seconds = sum(q.time_limit_seconds for q in self.questions if q.time_limit_seconds)
        return total_seconds // 60  # Переводим в минуты

    @property
    def difficulty(self) -> str:
        """Сложность квиза (среднее арифметическое сложности вопросов)"""
        if not self.questions:
            return "easy"
        # Пока возвращаем среднее значение на основе баллов
        avg_points = sum(q.points for q in self.questions) / len(self.questions)
        if avg_points <= 2:
            return "easy"
        elif avg_points <= 5:
            return "medium"
        else:
            return "hard"

    @property
    def times_taken(self) -> int:
        """Количество прохождений квиза"""
        return len(self.quiz_results) if self.quiz_results else 0

    @property
    def cover_image_url(self) -> Optional[str]:
        """URL обложки квиза"""
        from ..crud import crud_media as media_crud
        from ..database.database import SessionLocal
        db = SessionLocal()
        media = media_crud.get_entity_primary_media(
            db, MediaEntity.QUIZ, self.id, MediaType.IMAGE
        )
        return media.url if media else None

    def __repr__(self):
        return f"<Quiz {self.title}>"

    @total_questions.setter
    def total_questions(self, value):
        self._total_questions = value
