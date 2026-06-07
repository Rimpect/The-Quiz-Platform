"""
Схемы для временных ответов (Redis)
"""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class UserAnswerCreate(BaseModel) :
    question_id: int
    answer_text: Optional[str] = None
    answer_id: Optional[int] = None
    answer_ids: Optional[List[int]] = None
    time_spent_seconds: Optional[int] = 0
    question_order: Optional[int] = 0


class UserAnswerUpdate(BaseModel) :
    answer_text: Optional[str] = None
    answer_id: Optional[int] = None
    answer_ids: Optional[List[int]] = None
    time_spent_seconds: Optional[int] = None


class UserAnswerResponse(BaseModel) :
    id: int
    session_id: str
    question_id: int
    answer_text: Optional[str]
    answer_ids: Optional[str]
    is_correct: bool
    points_earned: int
    time_spent_seconds: int
    created_at: datetime

    class Config :
        from_attributes = True


class SessionScoreResponse(BaseModel) :
    session_id: str
    total_points: int
    total_questions: int
    correct_answers: int
    max_points: int
    percentage: float


class StartSessionResponse(BaseModel) :
    session_id: str
    quiz_id: int
    total_questions: int
    expires_in_minutes: int = 60