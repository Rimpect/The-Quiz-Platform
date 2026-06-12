from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..crud import crud_achievement as achievement_crud
from ..database.database import get_db
from ..models.model_user import User
from ..schemas.schemas_response import ResponseFactory
from ..utils.security import get_current_user

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.get("")
def get_my_achievements(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Статус всех достижений текущего пользователя: {achievement_id: is_unlocked}"""
    achievement_crud.initialize_user_achievements(db, current_user.id)
    status = achievement_crud.get_all_achievements_status(db, current_user.id)
    return ResponseFactory.success(
        data={"achievements": {str(k): v for k, v in status.items()}},
        message="Achievements retrieved successfully"
    )


@router.post("/check")
def check_achievements(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Проверяет условия и разблокирует достижения. Возвращает список новых."""
    newly_unlocked = achievement_crud.check_and_unlock_achievements(db, current_user.id)
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
    achievement = achievement_crud.unlock_achievement(db, current_user.id, achievement_id)
    return ResponseFactory.success(
        data={"achievement_id": achievement.achievement_id, "is_unlocked": achievement.is_unlocked},
        message="Achievement unlocked"
    )
