# ========== Таблица 2: Квиз ==========
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base
import enum


class Difficulty(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuizMode(str, enum.Enum):
    SINGLE = "single"  # Одиночный режим
    TEAM = "team"  # Командный режим


class Quiz(Base):
    __tablename__ = "quizzes"

    # Основные поля
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)  # Название
    description = Column(Text, nullable=True)  # Описание

    # Визуальные элементы
    cover_url = Column(String(500), nullable=True)  # Обложка (путь к файлу)

    # Характеристики
    category = Column(String(100), nullable=True)  # Категория квиза
    characteristic = Column(Text, nullable=True)  # Подробная информация
    difficulty = Column(SQLEnum(Difficulty), default=Difficulty.MEDIUM)

    # Настройки квиза
    is_public = Column(Boolean, default=True)  # Публичность квиза
    quiz_mode = Column(SQLEnum(QuizMode), default=QuizMode.SINGLE)  # Режим команды/одиночный
    duration_minutes = Column(Integer, nullable=True)  # Длительность в минутах

    # Статистика
    #total_questions = Column(Integer, default=0)  # Количество вопросов (будет обновляться автоматически)
    #times_taken = Column(Integer, default=0)  # Количество прохождений

    # Метаданные
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    creator = relationship("User", foreign_keys=[created_by])
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    results = relationship("QuizResult", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")

    def __repr__(self) :
        return f"<Quiz {self.title}>"