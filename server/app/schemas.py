from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


# ========== Enums ==========
class ThemeMode(str, Enum):
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"

class QuizMode(str, Enum):
    SINGLE = "single"
    TEAM = "team"

class AnswerType(str, Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"
    TEXT = "text"
    NUMERIC = "numeric"


# ========== User Schemas ==========
class UserBase(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=50)
    theme_site: ThemeMode = ThemeMode.LIGHT
    login: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., email=True)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    nickname: Optional[str] = Field(None, min_length=1, max_length=50)
    theme_site: Optional[ThemeMode] = None
    photo_profile: Optional[str] = None
    email: Optional[str] = Field(None, email=True)

class User(UserBase):
    id: int
    photo_profile: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ========== Quiz Schemas ==========
class QuizBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    category: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    is_public: bool = True
    quiz_mode: QuizMode = QuizMode.SINGLE

class QuizCreate(QuizBase):
    cover_url: Optional[str] = None

class QuizUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    cover_url: Optional[str] = None
    is_public: Optional[bool] = None
    quiz_mode: Optional[QuizMode] = None

class Quiz(QuizBase):
    id: int
    cover_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    total_questions: int = 0
    duration_minutes: int = 0
    difficulty: str = "easy"
    times_taken: int = 0
    
    class Config:
        from_attributes = True


# ========== Question Schemas ==========
class QuestionBase(BaseModel):
    answer_type: AnswerType
    points: int = Field(1, ge=1, le=100)
    question_text: str = Field(..., min_length=1)
    media_url: Optional[str] = None
    time_limit_seconds: Optional[int] = Field(None, ge=5, le=300)

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    answer_type: Optional[AnswerType] = None
    points: Optional[int] = Field(None, ge=1, le=100)
    question_text: Optional[str] = Field(None, min_length=1)
    media_url: Optional[str] = None
    time_limit_seconds: Optional[int] = Field(None, ge=5, le=300)

class Question(QuestionBase):
    id: int
    quiz_id: int
    created_at: datetime
    updated_at: datetime
    answers: List['Answer'] = []
    
    class Config:
        from_attributes = True


# ========== Answer Schemas ==========
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

class Answer(AnswerBase):
    id: int
    question_id: int
    
    class Config:
        from_attributes = True


# ========== QuizResult Schemas ==========
class QuizResultBase(BaseModel):
    score: float = Field(0, ge=0)
    is_completed: bool = False
    max_score: float = Field(0, ge=0)

class QuizResultCreate(QuizResultBase):
    user_id: int
    quiz_id: int

class QuizResultUpdate(BaseModel):
    score: Optional[float] = Field(None, ge=0)
    is_completed: Optional[bool] = None
    completed_at: Optional[datetime] = None

class QuizResult(QuizResultBase):
    id: int
    user_id: int
    quiz_id: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_seconds: int = 0
    percentage: float = 0
    
    class Config:
        from_attributes = True


# ========== UserAnswer Schemas ==========
class UserAnswerCreate(BaseModel):
    question_id: int
    answer_text: Optional[str] = None
    answer_id: Optional[int] = None
    time_spent_seconds: Optional[int] = None

class UserAnswerResponse(BaseModel):
    id: int
    quiz_result_id: int
    question_id: int
    answer_text: Optional[str]
    answer_id: Optional[int]
    is_correct: bool
    points_earned: int
    time_spent_seconds: Optional[int]
    
    class Config:
        from_attributes = True


# ========== Auth Schemas ==========
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    login: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str


# Обновление ссылок
Question.model_rebuild()