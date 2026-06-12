"""
Импортирование всех моделей для SQLAlchemy
Это нужно чтобы Base.metadata.create_all() видела все таблицы
"""

from .model_user import User
from .model_quiz import Quiz
from .model_question import Question
from .model_answer import Answer
from .model_category import Category
from .model_achievement import UserAchievement
from .model_quiz_result import QuizResult
from .model_user_answer import UserAnswer
from .model_media import MediaEntity
from .model_guest import Guest
from .model_pending_quiz import PendingQuiz
from .model_game_session import GameSession, TeamMember, GameMode
from .model_JWT import JWTToken

__all__ = [
    "User",
    "Quiz",
    "Question",
    "Answer",
    "Category",
    "UserAchievement",
    "QuizResult",
    "UserAnswer",
    "MediaEntity",
    "Guest",
    "PendingQuiz",
    "GameSession",
    "TeamMember",
    "GameMode",
    "JWTToken",
]
