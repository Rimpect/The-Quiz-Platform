import os

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from ..database.database import get_db
from ..utils.logger import logger
from ..schemas.schemas_response import ResponseFactory, BaseResponse
from ..schemas.schemas_user import EmailRequest, AccessTokenStatusResponse, RefreshTokenResponse
from ..utils.security import create_access_token, create_refresh_token, get_current_user
from ..services.service_auth import AuthService


router = APIRouter(prefix="/auth", tags=["authentication"])

# Конфигурация cookie
COOKIE_SECURE = False  # True для HTTPS
COOKIE_HTTP_ONLY = True
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Dependency для получения экземпляра AuthService"""
    return AuthService(db)


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
        path="/api/auth"  # Только для auth эндпоинтов
    )


@router.post("/login")
def login(
        response: Response,
        email_data: EmailRequest,
        auth_service: AuthService = Depends(get_auth_service)
):
    """Вход пользователя - создание пары токенов"""
    result = auth_service.login(email_data.email, email_data.password)
    
    # Если результат содержит access_token, устанавливаем cookie
    if isinstance(result, dict) and "access_token" in result.get("data", {}):
        refresh_token = result["data"].get("access_token")  # Для простоты, в реальности нужен отдельный refresh_token
        # set_refresh_token_cookie(response, refresh_token, REFRESH_TOKEN_EXPIRE_DAYS)
    
    # Логируем вход (опционально)
    if isinstance(result, dict) and result.get("access_status") == "granted":
        user_id = result.get("data", {}).get("user_id")
        logger.info(f"User {user_id} logged")
    
    return result


@router.post("/refresh", response_model=BaseResponse)
def refresh_token(
        request: Request,
        response: Response,
        auth_service: AuthService = Depends(get_auth_service)
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

    # 2. Обновляем токен через сервис
    result = auth_service.refresh_tokens(refresh_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"access_status": "invalid", "error_message": "Invalid refresh token"}
        )

    # 3. Устанавливаем новый refresh токен в cookie
    set_refresh_token_cookie(response, result["refresh_token"], REFRESH_TOKEN_EXPIRE_DAYS)

    return RefreshTokenResponse(
        access_token=result["access_token"],
        token_type="bearer",
        access_status=result.get("access_status", "valid"),
        expires_in=result.get("expires_in", 30 * 60),
        message=result.get("message", "Token refreshed successfully")
    )


@router.post("/logout")
def logout(
        request: Request,
        response: Response,
        auth_service: AuthService = Depends(get_auth_service),
        current_user = Depends(get_current_user)
):
    """
    Выход пользователя - удаление refresh токена из cookie и отзыв токенов в БД
    """
    # 1. Получаем refresh токен из cookie
    refresh_token = request.cookies.get("refresh_token")

    # 2. Отзываем токен через сервис
    auth_service.logout(refresh_token, current_user.id)

    # 3. Очищаем refresh токен из cookie
    response.delete_cookie(
        key="refresh_token",
        path="/api/auth"
    )

    # 4. Возвращаем успешный ответ
    return ResponseFactory.success(
        message="Successfully logged out",
        data={
            "user_id": current_user.id,
            "nickname": current_user.nickname
        }
    )


@router.get("/verify", response_model=BaseResponse)
def verify_token(
        request: Request,
        auth_service: AuthService = Depends(get_auth_service)
):
    """
    Проверка статуса access токена
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return AccessTokenStatusResponse(
            access_status="missing",
            error_message="Access token is missing"
        )

    access_token = auth_header.split(" ")[1]
    verification = auth_service.verify_token(access_token)

    return AccessTokenStatusResponse(
        access_status=verification["status"],
        error_message=verification.get("error_message"),
        user_id=verification.get("user_id"),
        expires_at=verification.get("expires_at")
    )
