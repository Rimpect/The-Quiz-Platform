"""
Сервис для работы с категориями квизов.
Инкапсулирует бизнес-логику и использует CRUD для доступа к данным.
"""
from typing import List, Optional, Dict
from sqlalchemy.orm import Session

from ..crud import crud_categories


class CategoryService:
    """Сервис для работы с категориями"""

    def __init__(self, db: Session):
        self.db = db

    # ========== ПОЛУЧЕНИЕ ДАННЫХ ==========

    def get_all_categories(self) -> List[Dict]:
        """Получение всех категорий"""
        categories = crud_categories.get_all_categories(self.db)
        return [self._category_to_dict(c) for c in categories]

    def get_category(self, category_id: int) -> Optional[Dict]:
        """Получение категории по ID"""
        category = crud_categories.get_category(self.db, category_id)
        if not category:
            return None
        return self._category_to_dict(category)

    def get_category_by_type(self, category_type: str) -> Optional[Dict]:
        """Получение категории по типу"""
        category = crud_categories.get_category_by_type(self.db, category_type)
        if not category:
            return None
        return self._category_to_dict(category)

    # ========== СОЗДАНИЕ ==========

    def create_category(self, category_type: str) -> Dict:
        """Создание новой категории"""
        category = crud_categories.create_category(self.db, category_type)
        return self._category_to_dict(category)

    # ========== УДАЛЕНИЕ ==========

    def delete_category(self, category_id: int) -> bool:
        """Удаление категории"""
        return crud_categories.delete_category(self.db, category_id)

    # ========== ПРЕОБРАЗОВАНИЯ ==========

    def _category_to_dict(self, category) -> Dict:
        """Преобразование Category в dict для ответа"""
        return {
            "id": category.id,
            "category_type": category.category_type,
            "created_at": category.created_at.isoformat() if category.created_at else None,
        }
