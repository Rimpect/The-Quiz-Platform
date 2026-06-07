"""
Схемы для квизов и категорий
"""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


# ========== Категории ==========
class CategoryBase(BaseModel) :
    category_type: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class CategoryCreate(CategoryBase) :
    pass


class CategoryUpdate(BaseModel) :
    category_type: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None


class Category(CategoryBase) :
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config :
        from_attributes = True


class CategoryWithStats(Category) :
    quiz_count: int = 0


# ========== Квизы ==========
class QuizBase(BaseModel) :
    title: str = Field(..., min_length=1, max_length=200)
    category_id: Optional[int] = None
    description: str = Field(..., min_length=1)
    is_public: bool = True
    quiz_mode: str = "single"


class QuizCreate(QuizBase) :
    cover_url: Optional[str] = None


class QuizUpdate(BaseModel) :
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    category_id: Optional[int] = None
    description: Optional[str] = None
    cover_url: Optional[str] = None
    is_public: Optional[bool] = None
    quiz_mode: Optional[str] = None


class QuizResponse(QuizBase) :
    id: int
    cover_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    total_questions: int = 0
    duration_minutes: int = 0
    difficulty: str = "easy"
    times_taken: int = 0
    category_obj: Optional[Category] = None

    class Config :
        from_attributes = True


# ========== Массовое создание ==========
class AnswerBulkCreate(BaseModel) :
    answer_text: str = Field(..., min_length=1)
    is_correct: bool = False
    order_number: int = 0


class QuestionBulkCreate(BaseModel) :
    answer_type: str = Field(..., description="single/multiple/text/numeric")
    points: int = Field(1, ge=1, le=100)
    question_text: str = Field(..., min_length=1)
    media_url: Optional[str] = None
    time_limit_seconds: Optional[int] = Field(None, ge=5, le=300)
    answers: List[AnswerBulkCreate] = Field(default_factory=list)


class QuizBulkCreate(BaseModel) :
    title: str = Field(..., min_length=1, max_length=200)
    category_id: Optional[int] = None
    description: str = Field(..., min_length=1)
    cover_url: Optional[str] = None
    is_public: bool = True
    quiz_mode: str = "single"
    questions: List[QuestionBulkCreate] = Field(default_factory=list)


class QuizBulkResponse(BaseModel) :
    quiz_id: int
    title: str
    questions_created: int
    answers_created: int
    total_time_limit_minutes: int