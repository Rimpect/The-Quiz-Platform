import os

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from ..crud import crud_jwt_token as crud_jwt
from ..crud import crud_user as crud_user
from ..database.database import get_db
from ..utils.logger import logger

from ..models import model_user
from ..schemas import ResponseFactory
from ..utils.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_access_token,
    get_current_user,
    verify_refresh_token
)

from .. import schemas

router = APIRouter(prefix="/auth", tags=["authentication"])

# Конфигурация cookie
COOKIE_SECURE = False  # True для HTTPS
COOKIE_HTTP_ONLY = True
REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")


def set_refresh_token_cookie(response: Response, refresh_token: str, expires_days: int = 7):
    """Установка refresh токена в HttpOnly cookie"""
    expires = datetime.utcnow() + timedelta(days=expires_days)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=int(expires.timestamp()),
        httponly=COOKIE_HTTP_ONLY,
        secure=COOKIE_SECURE,
        samesite="lax",
        path="/api/auth"  # Только для auth эндпоинтов
    )


def clear_refresh_token_cookie(response: Response):
    """Очистка refresh токена из cookie"""
    response.delete_cookie(
        key="refresh_token",
        path="/api/auth"
    )


@router.post("/login", response_model=schemas.EmailResponse)
def login(
        response: Response,
        email_data: schemas.EmailRequest,
        db: Session = Depends(get_db)
):
    """Вход пользователя - создание пары токенов"""
    # Ищем пользователя
    user = crud_user.get_user_by_email(db, email_data.email)

    if not user or not verify_password(email_data.password, user.password_hash):
        return ResponseFactory.unauthorized(
            message="Invalid email or password",
            access_status="denied"
        )

    if not user.is_active:
        return ResponseFactory.forbidden(
            message="User account is disabled"
        )

    # Создаем токены
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    crud_jwt.create_token_pair(
        db=db,
        user_id=user.id,
        access_token=access_token,
        refresh_token=refresh_token,
    )

    # Устанавливаем refresh токен в HttpOnly cookie
    # Устанавливаем refresh_token в cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
        path="/api/auth"
    )

    # Логируем вход (опционально)
    logger.info(f"User {user.email} logged")

    return ResponseFactory.success(
        data={
            "access_token" : access_token,
            "token_type" : "bearer",
            "user_id" : user.id,
            "nickname" : user.nickname,
            "role" : user.role
        },
        message="Login successful",
        access_status="granted"
    )


@router.post("/refresh", response_model=schemas.RefreshTokenResponse)
def refresh_token(
        request: Request,
        response: Response,
        db: Session = Depends(get_db)
):
    """
    Обновление access токена
    Refresh токен берется из cookie, не нужно передавать в теле запроса
    """
    # 1. Получаем refresh токен из cookie
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"access_status": "missing", "error_message": "Refresh token not found in cookies"}
        )

    # 2. Проверяем refresh токен
    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"access_status": "invalid", "error_message": "Invalid refresh token"}
        )

    user_id = int(payload.get("sub"))

    # 3. Проверяем пользователя
    user = crud_user.get_user(db, user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"access_status": "invalid", "error_message": "User not found or inactive"}
        )

    # 4. Находим старую пару токенов
    old_token = crud_jwt.get_token_by_refresh(db, refresh_token)
    if not old_token or old_token.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"access_status": "invalid", "error_message": "Refresh token not found"}
        )

    # 5. Проверяем валидность refresh токена
    if not old_token.is_refresh_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"access_status": "expired", "error_message": "Refresh token is revoked or expired"}
        )

    # 6. Создаем новые токены
    new_access_token = create_access_token(data={"sub": str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    # 7. Отзываем старую пару
    crud_jwt.revoke_both_tokens(db, refresh_token, "Used for refresh")

    # 8. Создаем новую пару
    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None

    crud_jwt.create_token_pair(
        db=db,
        user_id=user.id,
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        user_agent=user_agent,
        ip_address=ip_address
    )

    # 9. Устанавливаем новый refresh токен в cookie
    set_refresh_token_cookie(response, new_refresh_token, REFRESH_TOKEN_EXPIRE_DAYS)

    # 10. Очищаем отработанные токены
    crud_jwt.cleanup_expired_tokens(db)

    return schemas.RefreshTokenResponse(
        access_token=new_access_token,
        token_type="bearer",
        access_status="valid",
        expires_in=30 * 60,
        message="Token refreshed successfully"
    )


@router.post("/logout")
def logout(
        request: Request,
        response: Response,
        db: Session = Depends(get_db),
        current_user: model_user.User = Depends(get_current_user)
):
    """
    Выход пользователя - удаление refresh токена из cookie и отзыв токенов в БД
    """
    # 1. Получаем refresh токен из cookie
    refresh_token = request.cookies.get("refresh_token")

    # 2. Если токен есть в cookie, отзываем его в БД
    if refresh_token:
        crud_jwt.revoke_both_tokens(
            db=db,
            refresh_token=refresh_token,
            reason=f"User {current_user.id} logged out"
        )

    # 3. Очищаем refresh токен из cookie
    response.delete_cookie(
        key="refresh_token",
        path="/api/auth",
        httponly=True,
        secure=False,  # True для HTTPS
        samesite="lax"
    )

    # 4. Возвращаем успешный ответ
    return ResponseFactory.success(
        message="Successfully logged out",
        data={
            "user_id": current_user.id,
            "nickname": current_user.nickname
        }
    )


@router.get("/verify", response_model=schemas.AccessTokenStatusResponse)
def verify_token(
        request: Request,
):
    """
    Проверка статуса access токена
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return schemas.AccessTokenStatusResponse(
            access_status="missing",
            error_message="Access token is missing"
        )

    access_token = auth_header.split(" ")[1]
    verification = verify_access_token(access_token)

    return schemas.AccessTokenStatusResponse(
        access_status=verification["status"],
        error_message=verification.get("error_message"),
        user_id=verification.get("user_id"),
        expires_at=verification.get("expires_at")
    )
