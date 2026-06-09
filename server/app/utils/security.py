"""
Модуль безопасности: JWT токены, хеширование паролей, аутентификация
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Type

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session


from ..crud import crud_guest as guest_crud
from ..crud import crud_user as user_crud
from ..database.database import get_db
from ..models import User

# ========== Конфигурация ==========
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# ========== Хеширование паролей ==========
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
security = HTTPBearer(auto_error=False)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хеширование пароля"""
    return pwd_context.hash(password)


# ========== Создание токенов ==========
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создание access токена"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """Создание refresh токена"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_guest_access_token(session_id: str, expires_hours: int = 24) -> str:
    """Создание access токена для гостя"""
    to_encode = {
        "sub": session_id,
        "type": "access",
        "is_guest": True,
        "exp": datetime.utcnow() + timedelta(hours=expires_hours)
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ========== Проверка токенов ==========
def verify_access_token(token: str, db: Session = None) -> Dict[str, Any]:
    """
    Проверка access токена с детальным статусом
    """
    result = {
        "status": "invalid",
        "error_message": None,
        "user_id": None,
        "is_guest": False,
        "guest_id": None,
        "payload": None,
        "expires_at": None
    }

    if not token:
        result["error_message"] = "Token is missing"
        return result

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "access":
            result["error_message"] = "Invalid token type"
            return result

        exp = payload.get("exp")
        if exp:
            result["expires_at"] = datetime.fromtimestamp(exp)
            if datetime.utcnow() > result["expires_at"]:
                result["status"] = "expired"
                result["error_message"] = "Token has expired"
                return result

        result["status"] = "valid"
        result["payload"] = payload
        result["is_guest"] = payload.get("is_guest", False)

        if result["is_guest"]:
            result["guest_id"] = payload.get("sub")
        else:
            result["user_id"] = int(payload.get("sub"))

    except jwt.ExpiredSignatureError:
        result["status"] = "expired"
        result["error_message"] = "Token has expired"
    except jwt.JWTError as e:
        result["error_message"] = f"Invalid token: {str(e)}"

    return result


def verify_refresh_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Проверка refresh токена

    Args:
        token: Refresh JWT токен

    Returns:
        Dict с payload если токен валиден, иначе None
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Проверяем тип токена
        if payload.get("type") != "refresh":
            return None

        # Проверяем срок действия
        exp = payload.get("exp")
        if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
            return None

        return payload

    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None


# ========== Получение текущего пользователя ==========
def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
) -> Type[User] :
    """Получение текущего пользователя (только зарегистрированные)"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    token = credentials.credentials
    verification = verify_access_token(token, db)

    if verification["status"] != "valid":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=verification["error_message"]
        )

    if verification["is_guest"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Guest users cannot access this resource"
        )

    user = user_crud.get_user(db, verification["user_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


def get_current_guest(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
):
    """Получение текущего гостя"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    token = credentials.credentials
    verification = verify_access_token(token, db)

    if verification["status"] != "valid":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=verification["error_message"]
        )

    if not verification["is_guest"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This endpoint is for guests only"
        )

    guest = guest_crud.get_guest_by_session(db, verification["guest_id"])
    if not guest:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Guest session not found"
        )

    if guest.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Guest session has expired"
        )

    return guest


def get_current_user_or_guest_optional(
        request: Request,
        db: Session = Depends(get_db)
) :
    """Получение текущего пользователя или гостя (опционально)"""
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer ") :
        return None

    token = auth_header.split(" ")[1]
    verification = verify_access_token(token, db)

    if verification["status"] != "valid" :
        return None

    if verification.get("is_guest") :
        return guest_crud.get_guest_by_session(db, verification["guest_id"])
    else :
        return user_crud.get_user(db, verification["user_id"])