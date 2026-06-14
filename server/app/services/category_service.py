"""Бизнес-логика категорий (HTTP-агностична: данные + доменные исключения)."""
from sqlalchemy.orm import Session

from ..crud import crud_categories
from ..models.model_user import User, UserRole
from ..schemas.schemas_quiz import CategoryResponse, CategoryCreate
from .exceptions import ForbiddenError, ConflictError, NotFoundError


def get_all_categories(db: Session):
    categories = crud_categories.get_all_categories(db)
    return [CategoryResponse.model_validate(c).model_dump() for c in categories]


def create_category(db: Session, category_data: CategoryCreate, current_user: User):
    if current_user.role != UserRole.ADMIN:
        raise ForbiddenError("Only admins can create categories")

    if crud_categories.get_category_by_type(db, category_data.category_type):
        raise ConflictError(f"Category '{category_data.category_type}' already exists")

    new_category = crud_categories.create_category(db, category_data.category_type)
    return CategoryResponse.model_validate(new_category).model_dump()


def delete_category(db: Session, category_id: int, current_user: User):
    if current_user.role != UserRole.ADMIN:
        raise ForbiddenError("Only admins can delete categories")

    if not crud_categories.get_category(db, category_id):
        raise NotFoundError(f"Category with id {category_id} not found")

    crud_categories.delete_category(db, category_id)
