import os
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models import model_user
from ..schemas.schemas_response import ResponseFactory, BaseResponse
from ..schemas.schemas_user import EmailRequest, RefreshTokenResponse
from ..services import auth_service
from ..utils.security import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])

# Конфигурация cookie (HTTP-слой)
COOKIE_SECURE = False  # True для HTTPS
COOKIE_HTTP_ONLY = True
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))


def set_refresh_token_cookie(response: Response, refresh_token: str,
                             expires_days: int = int(REFRESH_TOKEN_EXPIRE_DAYS)):
    """Установка refresh токена в HttpOnly cookie"""
    expires = datetime.utcnow() + timedelta(days=expires_days)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=int(expires.timestamp()),
        httponly=COOKIE_HTTP_ONLY,
        secure=COOKIE_SECURE,
        samesite="lax",
        path="/api/auth",
    )


def clear_refresh_token_cookie(response: Response):
    """Очистка refresh токена из cookie"""
    response.delete_cookie(key="refresh_token", path="/api/auth")


@router.post("/login")
def login(
        response: Response,
        email_data: EmailRequest,
        db: Session = Depends(get_db)
):
    """Вход пользователя - создание пары токенов"""
    data = auth_service.login(db, email_data.email, email_data.password)
    set_refresh_token_cookie(response, data["refresh_token"], REFRESH_TOKEN_EXPIRE_DAYS)
    return ResponseFactory.success(
        data={
            "access_token": data["access_token"],
            "token_type": "bearer",
            "user_id": data["user_id"],
            "nickname": data["nickname"],
            "role": data["role"],
            "photo_profile": data["photo_profile"],
        },
        message="Login successful",
        access_status="granted",
    )


@router.post("/refresh", response_model=BaseResponse)
def refresh_token(
        request: Request,
        response: Response,
        db: Session = Depends(get_db)
):
    """Обновление access токена. Refresh берётся из cookie."""
    cookie_token = request.cookies.get("refresh_token")
    tokens = auth_service.refresh_tokens(db, cookie_token)
    set_refresh_token_cookie(response, tokens["refresh_token"], REFRESH_TOKEN_EXPIRE_DAYS)
    return RefreshTokenResponse(
        access_token=tokens["access_token"],
        token_type="bearer",
        access_status="valid",
        expires_in=30 * 60,
        message="Token refreshed successfully",
    )


@router.post("/logout")
def logout(
        request: Request,
        response: Response,
        db: Session = Depends(get_db),
        current_user: model_user.User = Depends(get_current_user)
):
    """Выход пользователя - отзыв токенов и очистка cookie."""
    cookie_token = request.cookies.get("refresh_token")
    data = auth_service.logout(db, cookie_token, current_user)
    clear_refresh_token_cookie(response)
    return ResponseFactory.success(message="Successfully logged out", data=data)


@router.get("/verify", response_model=BaseResponse)
def verify_token(request: Request):
    """Проверка статуса access токена"""
    auth_header = request.headers.get("Authorization")
    token = (
        auth_header.split(" ")[1]
        if auth_header and auth_header.startswith("Bearer ")
        else None
    )
    return auth_service.check_access_token(token)
