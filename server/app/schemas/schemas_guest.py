from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


# ========== Гости ==========
class PromoteGuestRequest(BaseModel) :
    guest_id: int
    login: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class GuestCreate(BaseModel) :
    """Упрощённая схема для создания гостя (без nickname)"""
    expires_hours: int = Field(24, ge=1, le=168)


class GuestResponse(BaseModel):
    id: int
    nickname: str
    session_id: str
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    last_active_at: Optional[datetime] = None
    access_token: str
    token_type: str = "bearer"
