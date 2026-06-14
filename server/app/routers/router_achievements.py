from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models.model_user import User
from ..schemas.schemas_response import ResponseFactory
from ..utils.security import get_current_user
from ..services.service_achievement import AchievementService

router = APIRouter(prefix="/achievements", tags=["achievements"])


def get_achievement_service(db: Session = Depends(get_db)) -> AchievementService:
    """Dependency для получения экземпляра AchievementService"""
    return AchievementService(db)


@router.get("")
def get_my_achievements(
        achievement_service: AchievementService = Depends(get_achievement_service),
        current_user: User = Depends(get_current_user)
):
    """Статус всех достижений текущего пользователя: {achievement_id: is_unlocked}"""
    status = achievement_service.get_user_achievements(current_user.id)
    return ResponseFactory.success(
        data={"achievements": {str(k): v for k, v in status.items()}},
        message="Achievements retrieved successfully"
    )


@router.post("/check")
def check_achievements(
        achievement_service: AchievementService = Depends(get_achievement_service),
        current_user: User = Depends(get_current_user)
):
    """Проверяет условия и разблокирует достижения. Возвращает список новых."""
    newly_unlocked = achievement_service.check_and_unlock_achievements(current_user.id)
    return ResponseFactory.success(
        data={"newly_unlocked": newly_unlocked},
        message=f"Unlocked {len(newly_unlocked)} new achievement(s)"
    )


@router.post("/{achievement_id}/unlock")
def unlock_achievement(
        achievement_id: int,
        achievement_service: AchievementService = Depends(get_achievement_service),
        current_user: User = Depends(get_current_user)
):
    """Разблокировка конкретного достижения вручную"""
    achievement = achievement_service.unlock_achievement(current_user.id, achievement_id)
    return ResponseFactory.success(
        data=achievement,
        message="Achievement unlocked"
    )
