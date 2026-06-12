"""
Модель для игровой сессии (командные/рейтинговые квизы)
Хранится в памяти сервера, результаты сохраняются в БД
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base
import enum


class GameMode(str, enum.Enum):
    SOLO = "solo"
    COMPETITIVE = "competitive"  # рейтинговый
    TEAM = "team"  # командный


class GameSession(Base):
    """Модель для записи сессии в БД (для истории и статистики)"""
    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, nullable=False, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    game_mode = Column(SQLEnum(GameMode), default=GameMode.SOLO, nullable=False)

    # Для командных игр
    team_id = Column(String(100), nullable=True, index=True)
    team_name = Column(String(100), nullable=True)

    # Состояние игры
    current_question_index = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    question_start_time = Column(DateTime(timezone=True), nullable=True)

    # Времена
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)

    # Связи
    quiz = relationship("Quiz", foreign_keys=[quiz_id])

    def __repr__(self):
        return f"<GameSession id={self.session_id}, quiz={self.quiz_id}, mode={self.game_mode}>"


class TeamMember(Base):
    """Участник команды в игровой сессии"""
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), ForeignKey("game_sessions.session_id", ondelete="CASCADE"), nullable=False, index=True)
    team_id = Column(String(100), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Прогресс игрока
    current_score = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    user = relationship("User")

    def __repr__(self):
        return f"<TeamMember user={self.user_id}, team={self.team_id}>"
