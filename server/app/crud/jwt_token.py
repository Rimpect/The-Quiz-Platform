from datetime import datetime, timedelta
from typing import Optional, Type

from passlib.context import CryptContext
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from ..models.model_JWT import JWTToken

# Конфигурация
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # 15 минут для access токена
REFRESH_TOKEN_EXPIRE_DAYS = 7  # 7 дней для refresh токена

# Для хеширования токенов
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_token(token: str) -> str :
    return pwd_context.hash(token)


def verify_token_hash(token: str, hashed: str) -> bool :
    return pwd_context.verify(token, hashed)


def create_token_pair(
        db: Session,
        user_id: int,
        access_token: str,
        refresh_token: str,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None
) -> JWTToken :
    from datetime import datetime, timedelta

    access_hash = hash_token(access_token)
    refresh_hash = hash_token(refresh_token)

    db_token = JWTToken(
        user_id=user_id,
        access_token_hash=access_hash,
        refresh_token_hash=refresh_hash,
        access_expires_at=datetime.utcnow() + timedelta(minutes=30),
        refresh_expires_at=datetime.utcnow() + timedelta(days=7),
        user_agent=user_agent,
        ip_address=ip_address,
        created_at=datetime.utcnow(),
        last_used_at=datetime.utcnow()
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def get_token_by_refresh(db: Session, refresh_token: str) -> Optional[JWTToken] :
    """Получение токена по refresh токену"""
    tokens = db.query(JWTToken).filter(
        JWTToken.is_refresh_revoked == False
    ).all()

    for token in tokens :
        if verify_token_hash(refresh_token, token.refresh_token_hash) :
            return token
    return None


def revoke_both_tokens(db: Session, refresh_token: str, reason: str = "Revoked") -> bool :
    """Отзыв обоих токенов"""
    token = get_token_by_refresh(db, refresh_token)
    if token :
        token.is_access_revoked = True
        token.is_refresh_revoked = True
        token.revoked_at = datetime.utcnow()
        token.revoked_reason = reason
        db.commit()
        return True
    return False


def revoke_access_token_by_value(db: Session, access_token: str, reason: str = "Revoked") -> bool :
    """Отзыв access токена по его значению"""
    tokens = db.query(JWTToken).filter(
        JWTToken.is_access_revoked == False
    ).all()

    for token in tokens :
        if verify_token_hash(access_token, token.access_token_hash) :
            token.is_access_revoked = True
            token.revoked_at = datetime.utcnow()
            token.revoked_reason = reason
            db.commit()
            return True
    return False


def revoke_all_user_tokens(db: Session, user_id: int, reason: str = "All revoked") -> int :
    """Отзыв всех токенов пользователя"""
    result = db.query(JWTToken).filter(
        JWTToken.user_id == user_id,
        JWTToken.is_refresh_revoked == False
    ).update({
        "is_access_revoked" : True,
        "is_refresh_revoked" : True,
        "revoked_at" : datetime.utcnow(),
        "revoked_reason" : reason
    })
    db.commit()
    return result


def cleanup_expired_tokens(db: Session) -> int :
    """
    Удаление отработанных (истекших) токенов из БД
    """
    from datetime import datetime, timedelta

    # Токены, которые истекли более 1 дня назад
    threshold = datetime.utcnow() - timedelta(days=1)

    result = db.query(JWTToken).filter(
        JWTToken.refresh_expires_at < threshold
    ).delete()

    db.commit()
    return result


def is_access_token_revoked(db: Session, access_token: str) -> bool :
    """Проверка, отозван ли access токен"""
    tokens = db.query(JWTToken).filter(
        JWTToken.is_access_revoked == False
    ).all()

    for token in tokens :
        if verify_token_hash(access_token, token.access_token_hash) :
            return False
    return True
