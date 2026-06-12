"""
Схемы для вопросов
"""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from .schemas_answer import AnswerResponse


class QuestionBase(BaseModel):
    answer_type: str = Field(..., description="single or multiple")
    points: int = Field(1, ge=1, le=100)
    question_text: str = Field(..., min_length=1)
    media_url: Optional[str] = None
    time_limit_seconds: Optional[int] = Field(None, ge=5, le=300)


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    answer_type: Optional[str] = None
    points: Optional[int] = Field(None, ge=1, le=100)
    question_text: Optional[str] = Field(None, min_length=1)
    media_url: Optional[str] = None
    time_limit_seconds: Optional[int] = Field(None, ge=5, le=300)


class QuestionResponse(QuestionBase):
    id: int
    quiz_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    answers: List[AnswerResponse] = []

    class Config:
        from_attributes = True