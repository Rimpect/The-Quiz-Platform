from sqlalchemy.orm import Session

from ..crud import crud_guest as guest_crud
from ..models.model_guest import Guest
from ..utils.security import create_guest_access_token
from .exceptions import ForbiddenError

def register_guest(db: Session):
    guest_user = guest_crud.create_guest(db=db, expires_hours=24)
    access_token = create_guest_access_token(guest_user.session_id, 24)
    return {
        "id": guest_user.id,
        "nickname": guest_user.nickname,
        "session_id": guest_user.session_id,
        "expires_at": guest_user.expires_at.isoformat(),
        "access_token": access_token,
        "token_type": "bearer",
    }

def get_guest_info(current_guest: Guest):
    return {
        "id": current_guest.id,
        "nickname": current_guest.nickname,
        "session_id": current_guest.session_id,
        "created_at": current_guest.created_at.isoformat() if current_guest.created_at else None,
        "expires_at": current_guest.expires_at.isoformat() if current_guest.expires_at else None,
        "last_active_at": current_guest.last_active_at.isoformat() if current_guest.last_active_at else None,
    }

def get_guest_stats(db: Session, current_user):
    if current_user.role != "admin":
        raise ForbiddenError("Admin access required")
    return guest_crud.get_guest_statistics(db)
