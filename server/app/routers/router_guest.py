from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from .. import schemas
from ..crud import crud_guest as guest_crud
from ..database.database import get_db
from ..models import model_guest as guest
from ..utils.security import create_guest_access_token, get_current_guest
from ..utils.security import get_current_user

router = APIRouter(prefix="/guest", tags=["guest"])


@router.post("/register", response_model=schemas.GuestResponse)
def register_guest(
        request: Request,
        guest_data: schemas.GuestCreate = None,
        db: Session = Depends(get_db)
):
    """Регистрация гостевого пользователя"""
    if guest_data is None:
        guest_data = schemas.GuestCreate()

    guest_user = guest_crud.create_guest(
        db=db,
        nickname=guest_data.nickname,
        expires_hours=guest_data.expires_hours
    )

    access_token = create_guest_access_token(guest_user.session_id, guest_data.expires_hours)

    return schemas.GuestResponse(
        id=guest_user.id,
        nickname=guest_user.nickname,
        session_id=guest_user.session_id,
        expires_at=guest_user.expires_at,
        access_token=access_token,
        token_type="bearer"
    )


@router.get("/me")
def get_guest_info(
        current_guest: guest = Depends(get_current_guest),
):
    """Получение информации о текущем госте"""
    return {
        "id": current_guest.id,
        "nickname": current_guest.nickname,
        "session_id": current_guest.session_id,
        "created_at": current_guest.created_at,
        "expires_at": current_guest.expires_at,
        "last_active_at": current_guest.last_active_at
    }


@router.get("/stats")
def get_guest_stats(
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    """Статистика по гостям (только для админов)"""
    if current_user.role == "admin":
        return guest_crud.get_guest_statistics(db)
    else:
        raise HTTPException(status_code=400, detail="No admin rules")
