from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from ..crud import crud_user
from ..crud import crud_jwt_token
from ..utils.security import (
    verify_password, create_access_token, create_refresh_token,
    verify_refresh_token, verify_access_token
)
from ..schemas.schemas_response import ResponseFactory


class AuthService :
    """Сервис аутентификации"""

    def __init__(self, db: Session) :
        self.db = db

    def login(self, email: str, password: str, user_agent: str = None, ip: str = None):
        """Логин пользователя"""
        user = crud_user.get_user_by_email(self.db, email)
        if not user or not verify_password(password, user.password_hash):
            return ResponseFactory.unauthorized(
                message="Invalid email or password",
                access_status="denied"
            )

        if not user.is_active:
            return ResponseFactory.forbidden(
                message="User account is disabled"
            )

        # Создание токенов
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        # Сохранение refresh токена
        crud_jwt_token.create_token_pair(
            db=self.db,
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token,
            user_agent=user_agent,
            ip_address=ip
        )

        return ResponseFactory.success(
            data={
                "access_token": access_token,
                "token_type": "bearer",
                "user_id": user.id,
                "nickname": user.nickname,
                "role": user.role,
                "photo_profile": getattr(user, "photo_profile", None)
            },
            message="Login successful",
            access_status="granted"
        )

    def refresh_tokens(self, refresh_token: str):
        """Обновление токенов"""
        payload = verify_refresh_token(refresh_token)
        if not payload:
            return None

        user_id = int(payload.get("sub"))
        user = crud_user.get_user(self.db, user_id)
        if not user:
            return None

        # Отзыв старого токена
        crud_jwt_token.revoke_both_tokens(self.db, refresh_token, "Used for refresh")

        # Создание новых
        new_access = create_access_token(data={"sub": str(user.id)})
        new_refresh = create_refresh_token(data={"sub": str(user.id)})

        crud_jwt_token.create_token_pair(
            db=self.db,
            user_id=user.id,
            access_token=new_access,
            refresh_token=new_refresh
        )

        return {
            "access_token": new_access,
            "refresh_token": new_refresh,
            "access_status": "valid",
            "expires_in": 30 * 60,
            "message": "Token refreshed successfully"
        }

    def logout(self, refresh_token: str, user_id: int) -> Dict:
        """Выход пользователя"""
        crud_jwt_token.revoke_both_tokens(self.db, refresh_token, f"User {user_id} logged out")
        return ResponseFactory.success(
            message="Successfully logged out",
            data={"user_id": user_id}
        )

    def verify_token(self, token: str) -> Dict[str, Any]:
        """Проверка токена"""
        return verify_access_token(token, self.db)

    def get_refresh_token_cookie_config(self) -> Dict:
        """Получение конфигурации для установки refresh токена в cookie"""
        return {
            "httponly": True,
            "secure": False,  # True для HTTPS
            "samesite": "lax",
            "path": "/api/auth",
            "max_age": int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7)) * 24 * 60 * 60
        }