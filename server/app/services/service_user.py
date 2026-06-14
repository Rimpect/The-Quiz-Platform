"""
Сервис для работы с пользователями.
Инкапсулирует бизнес-логику и использует CRUD для доступа к данным.
"""
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

from ..crud import crud_user
from ..schemas.schemas_user import UserCreate, UserUpdate, UserRole
from ..utils.security import verify_password, get_password_hash
from ..schemas.schemas_response import ResponseFactory


class UserService:
    """Сервис для работы с пользователями"""

    def __init__(self, db: Session):
        self.db = db

    # ========== ПОЛУЧЕНИЕ ДАННЫХ ==========

    def get_user(self, user_id: int) -> Optional[Dict]:
        """Получение пользователя по ID"""
        user = crud_user.get_user(self.db, user_id)
        if not user:
            return None
        return self._user_to_dict(user)

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Получение пользователя по email"""
        user = crud_user.get_user_by_email(self.db, email)
        if not user:
            return None
        return self._user_to_dict(user)

    def get_users(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Получение списка пользователей"""
        users = crud_user.get_users(self.db, skip=skip, limit=limit)
        return [self._user_to_dict(u) for u in users]

    def get_user_statistics(self, user_id: int) -> Dict[str, Any]:
        """Получение статистики пользователя"""
        return crud_user.get_user_statistics(self.db, user_id)

    # ========== СОЗДАНИЕ ПОЛЬЗОВАТЕЛЕЙ ==========

    def create_user(self, user_data: UserCreate) -> Dict:
        """Создание нового пользователя"""
        # Проверка на дубликат email
        existing = self.get_user_by_email(user_data.email)
        if existing:
            raise ValueError("Этот email уже зарегистрирован")

        user = crud_user.create_user(self.db, user_data)
        return self._user_to_dict(user)

    # ========== ОБНОВЛЕНИЕ ПОЛЬЗОВАТЕЛЕЙ ==========

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[Dict]:
        """Обновление данных пользователя"""
        user = crud_user.update_user(self.db, user_id, user_update)
        return self._user_to_dict(user) if user else None

    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """Смена пароля пользователя"""
        user = crud_user.get_user(self.db, user_id)
        if not user:
            raise ValueError("Пользователь не найден")

        if not verify_password(current_password, user.password_hash):
            raise ValueError("Неверный текущий пароль")

        user.password_hash = get_password_hash(new_password)
        self.db.commit()
        return True

    # ========== УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЕЙ ==========

    def delete_user(self, user_id: int) -> bool:
        """Удаление пользователя"""
        return crud_user.delete_user(self.db, user_id)

    # ========== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ==========

    def can_edit_user(self, user_id: int, current_user_id: int, user_role: str) -> bool:
        """Проверка прав на редактирование пользователя"""
        return user_id == current_user_id or user_role == UserRole.ADMIN

    def can_delete_user(self, user_id: int, current_user_id: int, user_role: str) -> bool:
        """Проверка прав на удаление пользователя"""
        return user_id == current_user_id or user_role == UserRole.ADMIN

    # ========== ПРЕОБРАЗОВАНИЯ ==========

    def _user_to_dict(self, user) -> Dict:
        """Преобразование User в dict для ответа"""
        return {
            "id": user.id,
            "nickname": user.nickname,
            "email": user.email,
            "role": user.role,
            "photo_profile": getattr(user, "photo_profile", None),
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        }
