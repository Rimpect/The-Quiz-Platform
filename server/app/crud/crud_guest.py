import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from ..models.model_guest import Guest


def create_guest(
        db: Session,
        expires_hours: int = 24
) -> Guest:
    """Создание нового гостя с обезличенным ником"""
    # Генерация уникального session_id
    session_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=expires_hours)

    # Фиксированный никнейм "Гость" + короткий идентификатор для различия
    short_id = session_id[:6]
    nickname = f"Гость_{short_id}"

    db_guest = Guest(
        nickname=nickname,
        session_id=session_id,
        expires_at=expires_at
    )
    db.add(db_guest)
    db.commit()
    db.refresh(db_guest)
    return db_guest


def get_guest(db: Session, guest_id: int):
    return db.query(Guest).filter(Guest.id == guest_id).first()


def get_guest_by_session(db: Session, session_id: str):
    return db.query(Guest).filter(Guest.session_id == session_id).first()


def get_active_guests(db: Session):
    """Получение активных (не истекших) гостей"""
    now = datetime.utcnow()
    return db.query(Guest).filter(Guest.expires_at > now).all()


def update_guest_activity(db: Session, guest_id: int) -> bool:
    """Обновление времени последней активности"""
    guest_user = get_guest(db, guest_id)
    if guest_user:
        guest_user.last_active_at = datetime.utcnow()
        db.commit()
        return True
    return False


def delete_expired_guests(db: Session) -> int:
    """Удаление истекших гостей"""
    now = datetime.utcnow()
    result = db.query(Guest).filter(Guest.expires_at < now).delete()
    db.commit()
    return result


def get_guest_statistics(db: Session) -> dict:
    """Статистика по гостям"""
    now = datetime.utcnow()
    total = db.query(Guest).count()
    active = db.query(Guest).filter(Guest.expires_at > now).count()
    expired = total - active

    return {
        "total_guests": total,
        "active_guests": active,
        "expired_guests": expired
    }