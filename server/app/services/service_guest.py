"""
Сервис для работы с гостевыми пользователями.
Инкапсулирует бизнес-логику и использует CRUD для доступа к данным.
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from ..crud import crud_guest


class GuestService:
    """Сервис для работы с гостевыми пользователями"""

    def __init__(self, db: Session):
        self.db = db

    # ========== РЕГИСТРАЦИЯ ==========

    def register_guest(self, expires_hours: int = 24) -> Dict:
        """Регистрация гостевого пользователя"""
        guest = crud_guest.create_guest(self.db, expires_hours=expires_hours)
        return {
            "id": guest.id,
            "nickname": guest.nickname,
            "session_id": guest.session_id,
            "expires_at": guest.expires_at.isoformat() if guest.expires_at else None,
        }

    # ========== ПОЛУЧЕНИЕ ДАННЫХ ==========

    def get_guest(self, session_id: str) -> Optional[Dict]:
        """Получение информации о госте"""
        guest = crud_guest.get_guest_by_session_id(self.db, session_id)
        if not guest:
            return None
        return self._guest_to_dict(guest)

    def get_guest_statistics(self) -> Dict[str, Any]:
        """Статистика по гостям"""
        return crud_guest.get_guest_statistics(self.db)

    # ========== ПРЕОБРАЗОВАНИЯ ==========

    def _guest_to_dict(self, guest) -> Dict:
        """Преобразование Guest в dict для ответа"""
        return {
            "id": guest.id,
            "nickname": guest.nickname,
            "session_id": guest.session_id,
            "created_at": guest.created_at.isoformat() if guest.created_at else None,
            "expires_at": guest.expires_at.isoformat() if guest.expires_at else None,
            "last_active_at": guest.last_active_at.isoformat() if guest.last_active_at else None,
        }
