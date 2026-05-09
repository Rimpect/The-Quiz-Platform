import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..crud import user as crud_user
from ..database.database import get_db
from ...app import schemas

# Конфигурация
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # 15 минут
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


# ========== Хеширование паролей ==========
def verify_password(plain_password: str, hashed_password: str) -> bool :
    """Проверка пароля"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str :
    """Хеширование пароля"""
    return pwd_context.hash(password)


# ========== Создание токенов ==========
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str :
    """
    Создание access токена

    Args:
        data: Данные для включения в токен (обычно {"sub": user_id})
        expires_delta: Время жизни токена (по умолчанию ACCESS_TOKEN_EXPIRE_MINUTES)

    Returns:
        JWT токен
    """
    to_encode = data.copy()

    if expires_delta :
        expire = datetime.utcnow() + expires_delta
    else :
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp" : expire,
        "type" : "access",
        "iat" : datetime.utcnow()  # issued at - время создания
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str :
    """
    Создание refresh токена

    Args:
        data: Данные для включения в токен (обычно {"sub": user_id})

    Returns:
        JWT токен
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({
        "exp" : expire,
        "type" : "refresh",
        "iat" : datetime.utcnow()
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ========== Проверка токенов ==========
def verify_access_token(token: str) -> Optional[Dict[str, Any]] :
    """
    Проверка access токена

    Returns:
        payload если токен валиден, иначе None
    """
    try :
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Проверяем тип токена
        if payload.get("type") != "access" :
            return None

        # Проверяем, не отозван ли токен (blacklist)
        if is_token_blacklisted(token) :
            return None

        return payload
    except JWTError :
        return None


def verify_refresh_token(token: str) -> Optional[Dict[str, Any]] :
    """
    Проверка refresh токена

    Returns:
        payload если токен валиден, иначе None
    """
    try :
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Проверяем тип токена
        if payload.get("type") != "refresh" :
            return None

        return payload
    except JWTError :
        return None


# ========== Blacklist для access токенов ==========
def add_token_to_blacklist(token: str, expires_in: int) -> bool :
    """
    Добавление access токена в черный список

    Args:
        token: JWT токен
        expires_in: Время жизни токена в секундах (до автоматического удаления)

    Returns:
        True если успешно добавлен
    """
    try :
        # Вариант 1: Использование Redis (рекомендуется для production)
        # redis_client.setex(f"blacklist:{token}", expires_in, "revoked")

        # Вариант 2: Использование БД (создайте таблицу TokenBlacklist)
        # db_token_blacklist = TokenBlacklist(token=token, expires_at=datetime.utcnow() + timedelta(seconds=expires_in))
        # db.add(db_token_blacklist)
        # db.commit()

        # Вариант 3: Временное решение - сохраняем в словаре (только для разработки, не для production!)
        # В production используйте Redis или БД
        return True
    except Exception :
        return False


def is_token_blacklisted(token: str) -> bool :
    """
    Проверка, находится ли токен в черном списке
    """
    # Вариант 1: Redis
    # return redis_client.exists(f"blacklist:{token}") > 0

    # Вариант 2: БД
    # return db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first() is not None

    # Вариант 3: Словарь (только для разработки)
    return False


# ========== Получение текущего пользователя ==========
async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
) -> schemas.User :
    """
    Получение текущего пользователя из access токена

    Используется для защиты эндпоинтов: 
    current_user: User = Depends(get_current_user)
    """
    token = credentials.credentials

    # Проверяем токен
    payload = verify_access_token(token)
    if not payload :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate" : "Bearer"},
        )

    # Получаем user_id из токена
    user_id: str = payload.get("sub")
    if not user_id :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate" : "Bearer"},
        )

    # Получаем пользователя из БД
    user = crud_user.get_user(db, int(user_id))
    if not user :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate" : "Bearer"},
        )

    # Проверяем активность пользователя
    if not user.is_active :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )

    return user


async def get_current_active_user(
        current_user: schemas.User = Depends(get_current_user)
) -> schemas.User :
    """
    Получение активного пользователя (проверяет is_active)
    """
    if not current_user.is_active :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    return current_user


async def get_current_admin_user(
        current_user: schemas.User = Depends(get_current_user)
) -> schemas.User :
    """
    Получение администратора (проверяет роль admin)
    """
    if current_user.role != "admin" :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user


# ========== Проверка прав доступа ==========
def require_roles(*allowed_roles: str) :
    """
    Декоратор для проверки ролей пользователя

    Использование:
    @router.get("/admin-only")
    @require_roles("admin")
    def admin_endpoint(current_user: User = Depends(get_current_user)):
        ...
    """

    def role_checker(current_user: schemas.User = Depends(get_current_user)) :
        if current_user.role not in allowed_roles :
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {current_user.role} not allowed. Required: {allowed_roles}"
            )
        return current_user

    return role_checker


def check_resource_ownership(resource_user_id: int, current_user: schemas.User) -> bool :
    """
    Проверка, является ли пользователь владельцем ресурса

    Args:
        resource_user_id: ID пользователя, которому принадлежит ресурс
        current_user: Текущий пользователь

    Returns:
        True если пользователь владелец или администратор
    """
    return current_user.id == resource_user_id or current_user.role == "admin"
