"""Бизнес-логика аутентификации (HTTP-агностична).

Работа с cookie/Request/Response остаётся в роутере — это HTTP-слой. Здесь —
проверка кредов, выпуск/ротация/отзыв токенов, статус access-токена.
"""
from sqlalchemy.orm import Session

from ..crud import crud_jwt_token as crud_jwt
from ..crud import crud_user
from ..utils.logger import logger
from ..utils.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    verify_access_token,
)
from ..schemas.schemas_user import AccessTokenStatusResponse
from .exceptions import UnauthorizedError, ForbiddenError


def login(db: Session, email: str, password: str) -> dict:
    user = crud_user.get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        raise UnauthorizedError("Invalid email or password")
    if not user.is_active:
        raise ForbiddenError("User account is disabled")

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    crud_jwt.create_token_pair(
        db=db, user_id=user.id, access_token=access_token, refresh_token=refresh_token
    )
    logger.info(f"User {user.email} logged")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_id": user.id,
        "nickname": user.nickname,
        "role": user.role,
        "photo_profile": user.photo_profile,
    }


def refresh_tokens(db: Session, refresh_token: str) -> dict:
    if not refresh_token:
        raise UnauthorizedError("Refresh token not found in cookies")

    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise UnauthorizedError("Invalid refresh token")

    user_id = int(payload.get("sub"))
    user = crud_user.get_user(db, user_id)
    if not user or not user.is_active:
        raise UnauthorizedError("User not found or inactive")

    old_token = crud_jwt.get_token_by_refresh(db, refresh_token)
    if not old_token or old_token.user_id != user_id:
        raise UnauthorizedError("Refresh token not found")
    if not old_token.is_refresh_valid:
        raise UnauthorizedError("Refresh token is revoked or expired")

    new_access_token = create_access_token(data={"sub": str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})
    crud_jwt.revoke_both_tokens(db, refresh_token, "Used for refresh")
    crud_jwt.create_token_pair(
        db=db, user_id=user.id, access_token=new_access_token, refresh_token=new_refresh_token
    )
    crud_jwt.cleanup_expired_tokens(db)

    return {"access_token": new_access_token, "refresh_token": new_refresh_token}


def logout(db: Session, refresh_token: str, current_user) -> dict:
    if refresh_token:
        crud_jwt.revoke_both_tokens(
            db=db, refresh_token=refresh_token,
            reason=f"User {current_user.id} logged out",
        )
    return {"user_id": current_user.id, "nickname": current_user.nickname}


def check_access_token(access_token) -> AccessTokenStatusResponse:
    if not access_token:
        return AccessTokenStatusResponse(
            access_status="missing", error_message="Access token is missing"
        )
    verification = verify_access_token(access_token)
    return AccessTokenStatusResponse(
        access_status=verification["status"],
        error_message=verification.get("error_message"),
        user_id=verification.get("user_id"),
        expires_at=verification.get("expires_at"),
    )
