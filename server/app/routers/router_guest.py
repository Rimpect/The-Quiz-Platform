from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models.model_guest import Guest
from ..schemas.schemas_response import ResponseFactory
from ..services import guest_service
from ..utils.security import get_current_guest, get_current_user

router = APIRouter(prefix="/guest", tags=["guest"])


@router.post("/register")
def register_guest(db: Session = Depends(get_db)):
    """Регистрация гостевого пользователя (без ввода никнейма)"""
    data = guest_service.register_guest(db)
    return ResponseFactory.success(
        data=data,
        message="Guest registered successfully",
        access_status="guest",
    )


@router.get("/me")
def get_guest_info(current_guest: Guest = Depends(get_current_guest)):
    """Получение информации о текущем госте"""
    data = guest_service.get_guest_info(current_guest)
    return ResponseFactory.success(
        data=data,
        message="Guest info retrieved",
        access_status="guest",
    )


@router.get("/stats")
def get_guest_stats(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """Статистика по гостям (только для админов)"""
    stats = guest_service.get_guest_stats(db, current_user)
    return ResponseFactory.success(data=stats, message="Guest statistics retrieved")
