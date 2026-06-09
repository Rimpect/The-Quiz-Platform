from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session


from ..crud import crud_guest as guest_crud
from ..database.database import get_db
from ..models.model_guest import Guest
from ..schemas.schemas_response import ResponseFactory
from ..utils.security import create_guest_access_token, get_current_guest
from ..utils.security import get_current_user

router = APIRouter(prefix="/guest", tags=["guest"])


@router.post("/register")
def register_guest(
        db: Session = Depends(get_db)
):
    """Регистрация гостевого пользователя (без ввода никнейма)"""
    # Создаём гостя с системным ником
    guest_user = guest_crud.create_guest(
        db=db,
        expires_hours=24
    )

    access_token = create_guest_access_token(guest_user.session_id, 24)

    return ResponseFactory.success(
        data={
            "id" : guest_user.id,
            "nickname" : guest_user.nickname,
            "session_id" : guest_user.session_id,
            "expires_at" : guest_user.expires_at.isoformat(),
            "access_token" : access_token,
            "token_type" : "bearer"
        },
        message="Guest registered successfully",
        access_status="guest"
    )


@router.get("/me")
def get_guest_info(
        current_guest: Guest = Depends(get_current_guest),
) :
    """Получение информации о текущем госте"""
    return ResponseFactory.success(
        data={
            "id" : current_guest.id,
            "nickname" : current_guest.nickname,
            "session_id" : current_guest.session_id,
            "created_at" : current_guest.created_at.isoformat() if current_guest.created_at else None,
            "expires_at" : current_guest.expires_at.isoformat() if current_guest.expires_at else None,
            "last_active_at" : current_guest.last_active_at.isoformat() if current_guest.last_active_at else None
        },
        message="Guest info retrieved",
        access_status="guest"
    )


@router.get("/stats")
def get_guest_stats(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
) :
    """Статистика по гостям (только для админов)"""
    if current_user.role != "admin" :
        return ResponseFactory.forbidden(
            message="Admin access required"
        )

    stats = guest_crud.get_guest_statistics(db)
    return ResponseFactory.success(
        data=stats,
        message="Guest statistics retrieved"
    )