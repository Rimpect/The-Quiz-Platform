# ========== Таблица 2: Квиз ==========
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base
import enum
from model_question import Question
from model_statistic import QuizResult

class Difficulty(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuizMode(str, enum.Enum):
    SINGLE = "single"  # Одиночный режим
    TEAM = "team"  # Командный режим


class Quiz(Base) :
    __tablename__ = "quizzes"

    # Обязательные поля
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)  # Название
    category = Column(String(100), nullable=False)  # Категория
    description = Column(Text, nullable=False)  # Описание
    cover_url = Column(String(500), nullable=True)  # Обложка (путь к файлу)
    is_public = Column(Boolean, default=True, nullable=False)  # Публичность квиза
    quiz_mode = Column(SQLEnum(QuizMode), default=QuizMode.SINGLE, nullable=False)  # Режим команды
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # Дата создания
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)  # Дата изменения

    # Вычисляемые поля без сохранения 
    # duration_minutes - вычисляется из вопросов
    # total_questions - вычисляется из вопросов
    # difficulty - вычисляется на основе вопросов
    # times_taken - вычисляется из статистики прохождений

    # Связи
    questions = relationship(Question, back_populates="quiz", cascade="all, delete-orphan")
    results = relationship(QuizResult, back_populates="quiz", cascade="all, delete-orphan")

    # Вычисляемые свойства (property)
    @property
    def total_questions(self) -> int :
        """Количество вопросов в квизе"""
        return len(self.questions) if self.questions else 0

    @property
    def duration_minutes(self) -> int :
        """Длительность квиза в минутах (сумма времени ожидания ответа на все вопросы)"""
        if not self.questions :
            return 0
        total_seconds = sum(q.time_limit_seconds for q in self.questions if q.time_limit_seconds)
        return total_seconds // 60  # Переводим в минуты

    @property
    def difficulty(self) -> str :
        """Сложность квиза (среднее арифметическое сложности вопросов)"""
        if not self.questions :
            return "easy"
        # Если у вас есть поле difficulty в вопросах, можно усреднять
        # Пока возвращаем среднее значение на основе баллов
        avg_points = sum(q.points for q in self.questions) / len(self.questions)
        if avg_points <= 2 :
            return "easy"
        elif avg_points <= 5 :
            return "medium"
        else :
            return "hard"

    @property
    def times_taken(self) -> int:
        """Количество прохождений квиза"""
        return len(self.results) if self.results else 0

    def __repr__(self) :
        return f"<Quiz {self.title}>"