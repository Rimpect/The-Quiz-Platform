from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List
import uuid

from ..models import model_guest as guest

def create_guest(
        db: Session,
        nickname: str = None,
        ip_address: str = None,
        user_agent: str = None,
        expires_hours: int = 24
) -> guest :
    """Создание нового гостя"""
    if not nickname :
        nickname = f"Guest_{uuid.uuid4().hex[:8]}"

    # Проверяем уникальность никнейма среди гостей
    base_nickname = nickname
    counter = 1
    while db.query(guest).filter(guest.nickname == nickname).first() :
        nickname = f"{base_nickname}_{counter}"
        counter += 1

    session_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=expires_hours)

    db_guest = guest
    db.add(db_guest)
    db.commit()
    db.refresh(db_guest)
    return db_guest


def get_guest(db: Session, guest_id: int) -> guest:
    return db.query(guest).filter(guest.id == guest_id).first()


def get_guest_by_session(db: Session, session_id: str) -> guest:
    return db.query(guest).filter(guest.session_id == session_id).first()


def get_active_guests(db: Session) -> [guest]:
    """Получение активных (не истекших) гостей"""
    now = datetime.utcnow()
    return db.query(guest).filter(guest.expires_at > now).all()


def update_guest_activity(db: Session, guest_id: int) -> bool :
    """Обновление времени последней активности"""
    guest = get_guest(db, guest_id)
    if guest :
        guest.last_active_at = datetime.utcnow()
        db.commit()
        return True
    return False


def delete_expired_guests(db: Session) -> int :
    """Удаление истекших гостей"""
    now = datetime.utcnow()
    result = db.query(guest).filter(guest.expires_at < now).delete()
    db.commit()
    return result


def get_guest_statistics(db: Session) -> dict :
    """Статистика по гостям"""
    now = datetime.utcnow()
    total = db.query(guest).count()
    active = db.query(guest).filter(guest.expires_at > now).count()
    expired = total - active

    return {
        "total_guests" : total,
        "active_guests" : active,
        "expired_guests" : expired
    }