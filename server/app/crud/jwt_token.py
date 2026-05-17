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
    """Хеширование токена для хранения в БД"""
    return pwd_context.hash(token)


def verify_token(token: str, hashed: str) -> bool :
    """Проверка токена с хешем в БД"""
    return pwd_context.verify(token, hashed)


def create_token_pair(
        db: Session,
        user_id: int,
        access_token: str,
        refresh_token: str,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None
) -> JWTToken :
    """
    Создание пары токенов (access + refresh) для пользователя
    """
    # Хешируем токены
    access_hash = hash_token(access_token)
    refresh_hash = hash_token(refresh_token)

    # Устанавливаем даты истечения
    now = datetime.utcnow()
    access_expires = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expires = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    db_token = JWTToken(
        user_id=user_id,
        access_token_hash=access_hash,
        refresh_token_hash=refresh_hash,
        access_expires_at=access_expires,
        refresh_expires_at=refresh_expires,
        user_agent=user_agent,
        ip_address=ip_address,
        last_used_at=now
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def get_token_by_refresh(db: Session, refresh_token: str) -> Optional[Type[JWTToken]] :
    """
    Получение записи токена по refresh токену
    """
    # Получаем все не отозванные refresh токены
    tokens = db.query(JWTToken).filter(
        JWTToken.is_refresh_revoked == False
    ).all()

    # Ищем совпадение по хешу
    for token in tokens :
        if verify_token(refresh_token, token.refresh_token_hash) :
            return token
    return None


def get_token_by_access(db: Session, access_token: str) -> Optional[Type[JWTToken]] :
    """
    Получение записи токена по access токену
    """
    # Получаем все не отозванные access токены
    tokens = db.query(JWTToken).filter(
        JWTToken.is_access_revoked == False
    ).all()

    # Ищем совпадение по хешу
    for token in tokens :
        if verify_token(access_token, token.access_token_hash) :
            return token
    return None


def get_token_by_id(db: Session, token_id: int) -> Optional[JWTToken] :
    """Получение токена по ID"""
    return db.query(JWTToken).filter(JWTToken.id == token_id).first()


def get_user_active_tokens(db: Session, user_id: int) -> list[Type[JWTToken]] :
    """
    Получение всех активных токенов пользователя
    """
    now = datetime.utcnow()
    return db.query(JWTToken).filter(
        JWTToken.user_id == user_id,
        JWTToken.is_access_revoked == False,
        JWTToken.is_refresh_revoked == False,
        JWTToken.access_expires_at > now
    ).order_by(JWTToken.created_at.desc()).all()


def get_user_tokens_history(db: Session, user_id: int, limit: int = 50) -> list[Type[JWTToken]] :
    """
    Получение истории токенов пользователя (включая отозванные)
    """
    return db.query(JWTToken).filter(
        JWTToken.user_id == user_id
    ).order_by(JWTToken.created_at.desc()).limit(limit).all()


def refresh_access_token(
        db: Session,
        old_refresh_token: str,
        new_access_token: str,
        new_refresh_token: str
) -> Optional[JWTToken] :
    """
    Обновление пары токенов (создание новой пары, отзыв старой)

    Returns:
        Новая запись токена или None
    """
    # Находим старую запись
    old_token = get_token_by_refresh(db, old_refresh_token)
    if not old_token or not old_token.is_refresh_valid :
        return None

    # Отзываем старую пару
    old_token.revoke_both(reason="Refreshed with new tokens")
    db.commit()

    # Создаем новую пару
    new_token = JWTToken(
        user_id=old_token.user_id,
        access_token_hash=hash_token(new_access_token),
        refresh_token_hash=hash_token(new_refresh_token),
        access_expires_at=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        refresh_expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        user_agent=old_token.user_agent,
        ip_address=old_token.ip_address,
        last_used_at=datetime.utcnow()
    )
    db.add(new_token)
    db.commit()
    db.refresh(new_token)

    return new_token


def revoke_access_token(db: Session, access_token: str, reason: str = "Revoked") -> bool :
    """
    Отзыв access токена
    """
    token = get_token_by_access(db, access_token)
    if token:
        token.revoke_access(reason)
        db.commit()
        return True
    return False


def revoke_refresh_token(db: Session, refresh_token: str, reason: str = "Revoked") -> bool :
    """
    Отзыв refresh токена
    """
    token = get_token_by_refresh(db, refresh_token)
    if token :
        token.revoke_refresh(reason)
        db.commit()
        return True
    return False


def revoke_both_tokens(db: Session, refresh_token: str, reason: str = "Both revoked") -> bool :
    """
    Отзыв обоих токенов (access и refresh)
    """
    token = get_token_by_refresh(db, refresh_token)
    if token :
        token.revoke_both(reason)
        db.commit()
        return True
    return False


def revoke_all_user_tokens(db: Session, user_id: int, reason: str = "All tokens revoked") -> int :
    """
    Отзыв всех токенов пользователя
    """
    result = db.query(JWTToken).filter(
        JWTToken.user_id == user_id,
        or_(
            JWTToken.is_access_revoked == False,
            JWTToken.is_refresh_revoked == False
        )
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
    Очистка истекших токенов (помечаем как revoked)
    """
    now = datetime.utcnow()
    result = db.query(JWTToken).filter(
        or_(
            and_(JWTToken.access_expires_at < now, JWTToken.is_access_revoked == False),
            and_(JWTToken.refresh_expires_at < now, JWTToken.is_refresh_revoked == False)
        )
    ).update({
        "is_access_revoked" : True,
        "is_refresh_revoked" : True,
        "revoked_at" : now,
        "revoked_reason" : "Token expired"
    })
    db.commit()
    return result


def update_last_used(db: Session, token_id: int) -> bool :
    """
    Обновление времени последнего использования
    """
    token = get_token_by_id(db, token_id)
    if token :
        token.update_last_used()
        db.commit()
        return True
    return False


def get_token_statistics(db: Session, user_id: Optional[int] = None) -> dict :
    """
    Получение статистики по токенам
    """
    query = db.query(JWTToken)
    if user_id :
        query = query.filter(JWTToken.user_id == user_id)

    now = datetime.utcnow()

    total = query.count()
    active = query.filter(
        JWTToken.is_access_revoked == False,
        JWTToken.is_refresh_revoked == False,
        JWTToken.access_expires_at > now
    ).count()
    revoked_access = query.filter(JWTToken.is_access_revoked == True).count()
    revoked_refresh = query.filter(JWTToken.is_refresh_revoked == True).count()

    return {
        "total_tokens" : total,
        "active_sessions" : active,
        "revoked_access_tokens" : revoked_access,
        "revoked_refresh_tokens" : revoked_refresh,
        "expired_tokens" : query.filter(JWTToken.access_expires_at < now).count()
    }
