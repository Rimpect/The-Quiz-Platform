from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from ..crud import jwt_token as crud_jwt
from ..crud import user as crud_user
from ..database.database import get_db
from ..utils.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    get_current_user
)
from ...app import schemas

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
        request: Request,
        login_data: schemas.LoginRequest,
        db: Session = Depends(get_db)
) :
    """Вход пользователя - создание пары токенов"""
    # Ищем пользователя
    user = crud_user.get_user_by_login(db, login_data.login)
    if not user :
        user = crud_user.get_user_by_email(db, login_data.login)

    if not user or not verify_password(login_data.password, user.password_hash) :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Создаем токены
    access_token = create_access_token(data={"sub" : str(user.id)})
    refresh_token = create_refresh_token(data={"sub" : str(user.id)})

    # Сохраняем пару токенов в БД
    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None

    crud_jwt.create_token_pair(
        db=db,
        user_id=user.id,
        access_token=access_token,
        refresh_token=refresh_token,
        user_agent=user_agent,
        ip_address=ip_address
    )

    return {
        "access_token" : access_token,
        "refresh_token" : refresh_token,
        "token_type" : "bearer"
    }


@router.post("/refresh", response_model=schemas.Token)
def refresh_token(
        request: Request,
        refresh_data: schemas.RefreshTokenRequest,
        db: Session = Depends(get_db)
) :
    """Обновление access токена с помощью refresh токена"""
    # 1. Проверяем refresh токен
    payload = verify_refresh_token(refresh_data.refresh_token)
    if not payload :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user_id = int(payload.get("sub"))

    # 2. Проверяем пользователя
    user = crud_user.get_user(db, user_id)
    if not user or not user.is_active :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    # 3. Находим старую пару токенов
    old_token = crud_jwt.get_token_by_refresh(db, refresh_data.refresh_token)
    if not old_token or old_token.user_id != user_id :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found"
        )

    # 4. Проверяем валидность refresh токена
    if not old_token.is_refresh_valid :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is revoked or expired"
        )

    # 5. Создаем новые токены
    new_access_token = create_access_token(data={"sub" : str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub" : str(user.id)})

    # 6. Создаем новую пару и отзываем старую
    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None

    new_token = crud_jwt.refresh_access_token(
        db=db,
        old_refresh_token=refresh_data.refresh_token,
        new_access_token=new_access_token,
        new_refresh_token=new_refresh_token
    )

    if not new_token :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to refresh tokens"
        )

    # Опционально: обновляем метаданные (если изменились)
    new_token.user_agent = user_agent
    new_token.ip_address = ip_address
    db.commit()

    return {
        "access_token" : new_access_token,
        "refresh_token" : new_refresh_token,
        "token_type" : "bearer"
    }


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
        refresh_data: schemas.RefreshTokenRequest,
        db: Session = Depends(get_db)
) :
    """
    Выход пользователя - отзыв пары токенов
    """
    crud_jwt.revoke_both_tokens(
        db=db,
        refresh_token=refresh_data.refresh_token,
        reason="User logged out"
    )
    return None


@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
def logout_all_devices(
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)
) :
    """
    Выход со всех устройств - отзыв всех токенов пользователя
    """
    crud_jwt.revoke_all_user_tokens(
        db=db,
        user_id=current_user.id,
        reason="User logged out from all devices"
    )
    return None


@router.post("/revoke-access")
def revoke_access_token(
        refresh_data: schemas.RefreshTokenRequest,
        db: Session = Depends(get_db)
) :
    """
    Отзыв только access токена (refresh остается активным)
    """
    success = crud_jwt.revoke_access_token(
        db=db,
        access_token=refresh_data.refresh_token,  # TODO: передавать access токен отдельно
        reason="Access token revoked"
    )

    if not success :
        raise HTTPException(status_code=404, detail="Token not found")

    return {"message" : "Access token revoked"}


@router.get("/sessions")
def get_active_sessions(
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)
) :
    """
    Получение всех активных сессий пользователя
    """
    active_tokens = crud_jwt.get_user_active_tokens(db, current_user.id)

    sessions = []
    for token in active_tokens :
        sessions.append({
            "session_id" : token.id,
            "created_at" : token.created_at,
            "last_used_at" : token.last_used_at,
            "access_expires_at" : token.access_expires_at,
            "refresh_expires_at" : token.refresh_expires_at,
            "user_agent" : token.user_agent,
            "ip_address" : token.ip_address
        })

    return {"sessions" : sessions}


@router.get("/sessions/history")
def get_sessions_history(
        current_user: schemas.User = Depends(get_current_user),
        limit: int = 50,
        db: Session = Depends(get_db)
) :
    """
    Получение истории сессий (включая завершенные)
    """
    tokens = crud_jwt.get_user_tokens_history(db, current_user.id, limit)

    history = []
    for token in tokens :
        history.append({
            "session_id" : token.id,
            "created_at" : token.created_at,
            "revoked_at" : token.revoked_at,
            "revoked_reason" : token.revoked_reason,
            "was_access_valid" : token.is_access_valid,
            "was_refresh_valid" : token.is_refresh_valid,
            "user_agent" : token.user_agent,
            "ip_address" : token.ip_address
        })

    return {"history" : history}