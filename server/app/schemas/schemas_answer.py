"""
Схемы для ответов
"""
from pydantic import BaseModel, Field
from typing import Optional


class AnswerBase(BaseModel):
    answer_text: str = Field(..., min_length=1)
    is_correct: bool = False
    order_number: int = 0


class AnswerCreate(AnswerBase):
    pass


class AnswerUpdate(BaseModel):
    answer_text: Optional[str] = Field(None, min_length=1)
    is_correct: Optional[bool] = None
    order_number: Optional[int] = None


class AnswerResponse(AnswerBase):
    id: int
    question_id: int

    class Config:
        from_attributes = True