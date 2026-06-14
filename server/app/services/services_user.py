from sqlalchemy.orm import Session
from typing import Optional

from ..crud import crud_user
from ..crud import crud_achievement
from ..utils.security import get_password_hash, verify_password
from ..schemas.schemas_user import UserCreate, UserUpdate


class UserService :
    """Сервис для работы с пользователями"""

    def __init__(self, db: Session) :
        self.db = db

    def register_user(self, user_data: UserCreate) -> dict :
        """
        Регистрация нового пользователя
        Бизнес-логика: проверка email, хеширование, создание достижений
        """
        existing = crud_user.get_user_by_email(self.db, user_data.email)

        if existing :
            raise ValueError("Email already registered")

        password_hash = get_password_hash(user_data.password)

        user = crud_user.create_user(self.db, user_data, password_hash)

        crud_achievement.initialize_user_achievements(self.db, user.id)

        return {
            "id" : user.id,
            "nickname" : user.nickname,
            "email" : user.email,
            "role" : user.role.value
        }

    def get_user_profile(self, user_id: int) -> Optional[dict] :
        """Получение профиля пользователя"""
        user = crud_user.get_user(self.db, user_id)
        if not user :
            return None

        return {
            "id" : user.id,
            "nickname" : user.nickname,
            "email" : user.email,
            "role" : user.role.value,
            "created_at" : user.created_at,
            "is_active" : user.is_active
        }

    def update_user_profile(self, user_id: int, update_data: UserUpdate) -> Optional[dict] :
        """Обновление профиля (только разрешённые поля)"""
        allowed_fields = ["nickname", "email", "photo_profile"]
        filtered_data = {
            k : v for k, v in update_data.model_dump(exclude_unset=True).items()
            if k in allowed_fields and v is not None
        }

        if not filtered_data :
            return None

        user = crud_user.update_user(self.db, user_id, filtered_data)
        if not user :
            return None

        return {
            "id" : user.id,
            "nickname" : user.nickname,
            "email" : user.email
        }

    def change_user_password(self, user_id: int, current_password: str, new_password: str) -> bool :
        """Смена пароля с проверкой текущего"""
        user = crud_user.get_user(self.db, user_id)
        if not user :
            return False

        # Проверка текущего пароля
        if not verify_password(current_password, user.password_hash) :
            return False

        # Хеширование и сохранение нового
        new_hash = get_password_hash(new_password)
        return crud_user.update_password(self.db, user_id, new_hash)

    def delete_user_account(self, user_id: int) -> bool :
        """Удаление аккаунта (с проверкой связанных данных)"""
        return crud_user.delete_user(self.db, user_id)

    def get_user_statistics(self, user_id: int) -> dict :
        """Расчёт статистики пользователя"""
        raw_stats = crud_user.get_user_statistics_raw(self.db, user_id)
        results = raw_stats["results"]

        percentages = [
            round(r.score / r.max_score * 100, 1)
            for r in results
            if r.max_score and r.max_score > 0
        ]

        total_seconds = sum((r.duration_seconds or 0) for r in results)

        return {
            "total_quizzes_completed" : raw_stats["total_quizzes"],
            "average_score" : round(sum(percentages) / len(percentages), 1) if percentages else 0,
            "best_result" : max(percentages) if percentages else 0,
            "total_minutes" : round(total_seconds / 60)
        }