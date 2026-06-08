"""
Схемы для пользователей, аутентификации и гостей
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    GUEST = "guest"


class ThemeMode(str, Enum):
    LIGHT = "light"
    DARK = "dark"


# ========== Пользователи ==========
class User(BaseModel):
    email: Optional[EmailStr] = None
    password: str


class UserBase(BaseModel):
    theme_site: ThemeMode = ThemeMode.LIGHT
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    email: str = Field()
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    nickname: Optional[str] = Field(None, min_length=1, max_length=50)
    theme_site: Optional[ThemeMode] = None
    photo_profile: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    id: int
    photo_profile: Optional[str] = None
    role: UserRole
    is_guest: bool = False
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ========== Гости ==========
class GuestCreate(BaseModel):
    nickname: Optional[str] = Field(None, min_length=1, max_length=50)
    expires_hours: int = Field(24, ge=1, le=168)


class GuestResponse(BaseModel):
    id: int
    nickname: str
    role: UserRole
    is_guest: bool
    expires_at: Optional[datetime]
    access_token: str
    token_type: str = "bearer"


class PromoteGuestRequest(BaseModel):
    guest_id: int
    login: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


# ========== JWT и аутентификация ==========
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class EmailRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class EmailResponse(BaseModel):
    """Ответ после отправки email"""
    message: str = Field(..., description="Сообщение о результате")
    email: str = Field(..., description="Email получателя")
    status: str = Field("sent", description="Статус отправки")


class RefreshTokenResponse(BaseModel):
    """Ответ при обновлении токена"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(1800, description="Время жизни access токена в секундах")


class AccessTokenStatusResponse(BaseModel):
    access_status: str
    error_message: Optional[str] = None
    user_id: Optional[int] = None
    login: Optional[str] = None
    expires_at: Optional[datetime] = None
