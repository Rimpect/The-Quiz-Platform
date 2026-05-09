from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime
from jose import JWTError, jwt

from ..crud import user as crud_user
from ..crud import refresh_token as crud_refresh_token
from ...app import schemas
from ..database.database import get_db
from ..utils.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    SECRET_KEY,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS
)
from ..models.model_refresh_token import RefreshToken

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
        request: Request,
        login_data: schemas.LoginRequest,
        db: Session = Depends(get_db)
) :
    """Вход пользователя - создание access и refresh токенов"""
    # Ищем пользователя по логину или email
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

    # Получаем информацию об устройстве
    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None

    # Сохраняем refresh токен в БД (хешированным)
    crud_refresh_token.create_refresh_token(
        db=db,
        user_id=user.id,
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
    """
    Обновление access токена с помощью refresh токена

    Процесс:
    1. Проверяем валидность refresh токена (подпись, срок действия)
    2. Ищем токен в БД
    3. Проверяем, не отозван ли токен
    4. Проверяем, не истек ли токен
    5. Создаем новые токены
    6. Сохраняем новый refresh токен
    7. Отзываем старый refresh токен (одноразовый)
    """
    # 1. Проверяем валидность refresh токена
    try :
        payload = jwt.decode(
            refresh_data.refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Проверяем тип токена
        if payload.get("type") != "refresh" :
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        user_id = int(payload.get("sub"))
        if user_id is None :
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

    except JWTError as e :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid refresh token: {str(e)}"
        )

    # 2. Проверяем существование пользователя
    user = crud_user.get_user(db, user_id)
    if not user or not user.is_active :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    # 3. Ищем refresh токен в БД
    db_token = crud_refresh_token.get_refresh_token_by_value(db, refresh_data.refresh_token)
    if not db_token :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found in database"
        )

    # 4. Проверяем, не отозван ли токен
    if db_token.revoked_at is not None :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has been revoked"
        )

    # 5. Проверяем, не истек ли токен
    if db_token.expires_at < datetime.utcnow() :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired"
        )

    # 6. Проверяем соответствие пользователя
    if db_token.user_id != user_id :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token-user mismatch"
        )

    # 7. Создаем новые токены
    new_access_token = create_access_token(data={"sub" : str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub" : str(user.id)})

    # 8. Получаем информацию об устройстве
    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None

    # 9. Сохраняем новый refresh токен в БД
    new_db_token = crud_refresh_token.create_refresh_token(
        db=db,
        user_id=user.id,
        refresh_token=new_refresh_token,
        user_agent=user_agent,
        ip_address=ip_address
    )

    # 10. Отзываем старый refresh токен (одноразовое использование)
    crud_refresh_token.revoke_refresh_token(
        db=db,
        token_id=db_token.id,
        reason="Used for token refresh"
    )

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
    Выход пользователя - отзыв refresh токена
    """
    db_token = crud_refresh_token.get_refresh_token_by_value(db, refresh_data.refresh_token)
    if db_token :
        crud_refresh_token.revoke_refresh_token(
            db=db,
            token_id=db_token.id,
            reason="User logged out"
        )
    return None


@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
def logout_all_devices(
        current_user: schemas.User = Depends(get_current_user),  # Добавьте эту зависимость
        db: Session = Depends(get_db)
) :
    """
    Выход со всех устройств - отзыв всех refresh токенов пользователя
    """
    crud_refresh_token.revoke_all_user_tokens(
        db=db,
        user_id=current_user.id,
        reason="User logged out from all devices"
    )
    return None


@router.get("/sessions")
def get_active_sessions(
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)
) :
    """
    Получение всех активных сессий пользователя
    """
    active_tokens = crud_refresh_token.get_user_active_tokens(db, current_user.id)

    sessions = []
    for token in active_tokens :
        sessions.append({
            "session_id" : token.id,
            "created_at" : token.created_at,
            "last_used_at" : token.last_login,
            "expires_at" : token.expires_at,
            "user_agent" : token.user_agent,
            "ip_address" : token.ip_address,
            "is_current" : False  # Можно определить по текущему токену
        })

    return {"sessions" : sessions}


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_session(
        session_id: int,
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)
) :
    """
    Отзыв конкретной сессии по ID
    """
    token = crud_refresh_token.get_refresh_token_by_id(db, session_id)
    if not token or token.user_id != current_user.id :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    crud_refresh_token.revoke_refresh_token(
        db=db,
        token_id=session_id,
        reason="Session revoked by user"
    )
    return None