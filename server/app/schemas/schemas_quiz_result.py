"""
Схемы для результатов квизов
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class QuizResultBase(BaseModel) :
    score: float = Field(0, ge=0)
    is_completed: bool = False
    max_score: float = Field(0, ge=0)


class QuizResultCreate(QuizResultBase) :
    user_id: int
    quiz_id: int


class QuizResultUpdate(BaseModel) :
    score: Optional[float] = Field(None, ge=0)
    is_completed: Optional[bool] = None
    completed_at: Optional[datetime] = None


class QuizResultResponse(QuizResultBase) :
    id: int
    user_id: int
    quiz_id: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_seconds: int = 0
    percentage: float = 0

    class Config :
        from_attributes = True