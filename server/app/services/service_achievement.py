"""
Сервис для работы с достижениями.
Инкапсулирует бизнес-логику и использует CRUD для доступа к данным.
"""
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from ..crud import crud_achievement


class AchievementService:
    """Сервис для работы с достижениями"""

    def __init__(self, db: Session):
        self.db = db

    # ========== ПОЛУЧЕНИЕ ДАННЫХ ==========

    def get_user_achievements(self, user_id: int) -> Dict[str, bool]:
        """Получение статуса всех достижений пользователя"""
        crud_achievement.initialize_user_achievements(self.db, user_id)
        return crud_achievement.get_all_achievements_status(self.db, user_id)

    # ========== ПРОВЕРКА И РАЗБЛОКИРОВКА ==========

    def check_and_unlock_achievements(self, user_id: int) -> List[int]:
        """Проверка условий и разблокировка достижений"""
        return crud_achievement.check_and_unlock_achievements(self.db, user_id)

    def unlock_achievement(self, user_id: int, achievement_id: int) -> Dict:
        """Ручная разблокировка достижения"""
        achievement = crud_achievement.unlock_achievement(self.db, user_id, achievement_id)
        return {
            "achievement_id": achievement.achievement_id,
            "is_unlocked": achievement.is_unlocked,
        }
