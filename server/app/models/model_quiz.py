from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base
import enum


class QuizMode(str, enum.Enum) :
    SINGLE = "single"
    TEAM = "team"
    COMPETITIVE = "competitive"


class Quiz(Base) :
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)
    description = Column(Text, nullable=False)
    cover_url = Column(String(500), nullable=True)
    is_public = Column(Boolean, default=True, nullable=False)  # Одобренный квиз
    quiz_mode = Column(SQLEnum(QuizMode), default=QuizMode.SINGLE, nullable=False)

    # Кто создал
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    author = relationship("User")
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    quiz_results = relationship("QuizResult", back_populates="quiz", cascade="all, delete-orphan")
    category_ref = relationship("Category", back_populates="quizzes")

    @property
    def category(self) -> str :
        return self.category_ref.category_type if self.category_ref else None

    @property
    def total_questions(self) -> int :
        return len(self.questions) if self.questions else 0

    @property
    def duration_minutes(self) -> int :
        if not self.questions :
            return 0
        total_seconds = sum(q.time_limit_seconds or 0 for q in self.questions)
        return total_seconds // 60

    @property
    def times_taken(self) -> int :
        return len(self.results) if self.results else 0

    def __repr__(self) :
        return f"<Quiz {self.title}>"

    @total_questions.setter
    def total_questions(self, value) :
        self._total_questions = value