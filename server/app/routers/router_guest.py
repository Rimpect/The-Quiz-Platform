from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session


from ..database.database import get_db
from ..models import UserRole
from ..models.model_guest import Guest
from ..schemas.schemas_response import ResponseFactory
from ..utils.security import create_guest_access_token, get_current_guest, get_current_user
from ..services import GuestService

router = APIRouter(prefix="/guest", tags=["guest"])


def get_guest_service(db: Session = Depends(get_db)) -> GuestService:
    """Dependency для получения экземпляра GuestService"""
    return GuestService(db)


@router.post("/register")
def register_guest(
        guest_service: GuestService = Depends(get_guest_service)
):
    """Регистрация гостевого пользователя (без ввода никнейма)"""
    guest_data = guest_service.register_guest(expires_hours=24)

    access_token = create_guest_access_token(guest_data["session_id"], 24)

    return ResponseFactory.success(
        data={
            "id": guest_data["id"],
            "nickname": guest_data["nickname"],
            "session_id": guest_data["session_id"],
            "expires_at": guest_data["expires_at"],
            "access_token": access_token,
            "token_type": "bearer"
        },
        message="Guest registered successfully",
        access_status="guest"
    )


@router.get("/me")
def get_guest_info(
        current_guest: Guest = Depends(get_current_guest),
):
    """Получение информации о текущем госте"""
    return ResponseFactory.success(
        data={
            "id": current_guest.id,
            "nickname": current_guest.nickname,
            "session_id": current_guest.session_id,
            "created_at": current_guest.created_at.isoformat() if current_guest.created_at else None,
            "expires_at": current_guest.expires_at.isoformat() if current_guest.expires_at else None,
            "last_active_at": current_guest.last_active_at.isoformat() if current_guest.last_active_at else None
        },
        message="Guest info retrieved",
        access_status="guest"
    )


@router.get("/stats")
def get_guest_stats(
        guest_service: GuestService = Depends(get_guest_service),
        current_user=Depends(get_current_user)
):
    """Статистика по гостям (только для админов)"""
    if current_user.role != UserRole.ADMIN:
        return ResponseFactory.forbidden(
            message="Admin access required"
        )

    stats = guest_service.get_guest_statistics()
    return ResponseFactory.success(
        data=stats,
        message="Guest statistics retrieved"
    )