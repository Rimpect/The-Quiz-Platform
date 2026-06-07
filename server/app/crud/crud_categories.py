from typing import Optional

from sqlalchemy.orm import Session
from ..models.model_category import Category


def get_categories(db: Session, categories_id: int) -> Optional[Category]:
    return db.query(Category).filter(Category.id == categories_id).first()


def post_categories(db: Session, categories_id: int, category_type: str)\
        -> Optional[Category]:
    db_category = get_categories(db, categories_id)
    if db_category:
        db_category.category_type = category_type
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_categories(db: Session, categories_id: int) -> bool:
    db_categories = get_categories(db, categories_id)
    if db_categories:
        db.delete(db_categories)
        db.commit()
        return True
    return False
