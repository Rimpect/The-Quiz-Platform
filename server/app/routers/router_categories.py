from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..crud import crud_categories
from ..database.database import get_db
from ..schemas.schemas_quiz import CategoryResponse, CategoryCreate
from ..schemas.schemas_response import ResponseFactory
from ..utils.security import get_current_user
from ..models.model_user import User, UserRole

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/")
def get_all_categories(
        db: Session = Depends(get_db),
) :
    """Получение списка всех категорий (доступно всем)"""
    categories = crud_categories.get_all_categories(db)
    return ResponseFactory.success(
        data=[CategoryResponse.model_validate(c).model_dump() for c in categories],
        message="Categories retrieved successfully"
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category(
        category_data: CategoryCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) :
    """Создание новой категории (только для админов)"""
    if current_user.role != UserRole.ADMIN :
        return ResponseFactory.forbidden(
            message="Only admins can create categories"
        )

    existing = crud_categories.get_category_by_type(db, category_data.category_type)
    if existing :
        return ResponseFactory.conflict(
            message=f"Category '{category_data.category_type}' already exists"
        )

    new_category = crud_categories.create_category(db, category_data.category_type)
    return ResponseFactory.created(
        data=CategoryResponse.model_validate(new_category, from_attributes=True).model_dump(),
        message="Category created successfully"
    )


@router.delete("/{category_id}")
def delete_category(
        category_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) :
    """Удаление категории (только для админов)"""
    # ✅ Проверка прав
    if current_user.role != UserRole.ADMIN :
        return ResponseFactory.forbidden(
            message="Only admins can delete categories"
        )

    # ✅ Проверка существования
    category = crud_categories.get_category(db, category_id)
    if not category :
        return ResponseFactory.not_found(
            resource=f"Category with id {category_id}"
        )

    crud_categories.delete_category(db, category_id)
    return ResponseFactory.success(
        message="Category deleted successfully"
    )