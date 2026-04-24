from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import timedelta

from app import crud, schemas
from app.database import get_db
from app.utils.security import verify_password, create_access_token, create_refresh_token
from app.utils.jwt_utils import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
        login_data: schemas.LoginRequest,
        db: Session = Depends(get_db)
) :
    """Вход пользователя"""
    # Ищем пользователя по логину или email
    user = crud.get_user_by_login(db, login_data.login)
    if not user :
        user = crud.get_user_by_email(db, login_data.login)

    if not user or not verify_password(login_data.password, user.password_hash) :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Создаем токены
    access_token = create_access_token(data={"sub" : str(user.id)})
    refresh_token = create_refresh_token(data={"sub" : str(user.id)})

    return {
        "access_token" : access_token,
        "refresh_token" : refresh_token,
        "token_type" : "bearer"
    }


@router.post("/refresh", response_model=schemas.Token)
def refresh_token(
        refresh_data: schemas.RefreshTokenRequest,
        db: Session = Depends(get_db)
) :
    """Обновление access токена"""
    # Здесь должна быть проверка refresh токена
    # Временно возвращаем новый access токен
    return {
        "access_token" : "new_access_token",
        "refresh_token" : refresh_data.refresh_token,
        "token_type" : "bearer"
    }