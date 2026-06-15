from typing import Optional, List, Type
from sqlalchemy.orm import Session

# from ..models import Category
from ..models.model_category import Category


def get_all_categories(db: Session) -> List[Type[Category]]:
    return db.query(Category).all()


def get_category(db: Session, category_id: int) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_type(db: Session, category_type: str) -> Optional[Category]:
    """Получение категории по названию"""
    return db.query(Category).filter(Category.category_type == category_type).first()


def create_category(db: Session, category_type: str) -> Category:
    db_category = Category(category_type=category_type)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int) -> bool:
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False


DEFAULT_CATEGORIES = [
    "История", "География", "Литература", "Искусство", "Музыка",
    "Кино", "Наука", "Математика", "Технологии", "Спорт",
    "Психология", "Мифология", "Еда", "Животные", "Общая эрудиция",
]


def seed_default_categories(db: Session) -> int:
    created = 0
    for name in DEFAULT_CATEGORIES:
        if not get_category_by_type(db, name):
            create_category(db, name)
            created += 1
    return created
