"""Бизнес-логика достижений (HTTP-агностична)."""
from sqlalchemy.orm import Session

from ..crud import crud_achievement


def get_my_achievements(db: Session, current_user):
    crud_achievement.initialize_user_achievements(db, current_user.id)
    status = crud_achievement.get_all_achievements_status(db, current_user.id)
    return {"achievements": {str(k): v for k, v in status.items()}}


def check_achievements(db: Session, current_user):
    """Проверяет условия и разблокирует достижения. Возвращает список новых."""
    return crud_achievement.check_and_unlock_achievements(db, current_user.id)


def unlock_achievement(db: Session, current_user, achievement_id: int):
    achievement = crud_achievement.unlock_achievement(db, current_user.id, achievement_id)
    return {
        "achievement_id": achievement.achievement_id,
        "is_unlocked": achievement.is_unlocked,
    }
