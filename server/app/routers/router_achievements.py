from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models.model_user import User
from ..schemas.schemas_response import ResponseFactory
from ..services import achievement_service
from ..utils.security import get_current_user

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.get("")
def get_my_achievements(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Статус всех достижений текущего пользователя: {achievement_id: is_unlocked}"""
    data = achievement_service.get_my_achievements(db, current_user)
    return ResponseFactory.success(data=data, message="Achievements retrieved successfully")


@router.post("/check")
def check_achievements(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Проверяет условия и разблокирует достижения. Возвращает список новых."""
    newly_unlocked = achievement_service.check_achievements(db, current_user)
    return ResponseFactory.success(
        data={"newly_unlocked": newly_unlocked},
        message=f"Unlocked {len(newly_unlocked)} new achievement(s)"
    )


@router.post("/{achievement_id}/unlock")
def unlock_achievement(
        achievement_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Разблокировка конкретного достижения вручную"""
    data = achievement_service.unlock_achievement(db, current_user, achievement_id)
    return ResponseFactory.success(data=data, message="Achievement unlocked")
