from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..schemas.schemas_quiz import CategoryResponse, CategoryCreate
from ..schemas.schemas_response import ResponseFactory
from ..utils.security import get_current_user
from ..models.model_user import User, UserRole
from ..services.service_category import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    """Dependency для получения экземпляра CategoryService"""
    return CategoryService(db)


@router.get("")
def get_all_categories(
        category_service: CategoryService = Depends(get_category_service)
):
    """Получение списка всех категорий (доступно всем)"""
    categories = category_service.get_all_categories()
    return ResponseFactory.success(
        data=categories,
        message="Categories retrieved successfully"
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(
        category_data: CategoryCreate,
        category_service: CategoryService = Depends(get_category_service),
        current_user: User = Depends(get_current_user)
):
    """Создание новой категории (только для админов)"""
    if current_user.role != UserRole.ADMIN:
        return ResponseFactory.forbidden(
            message="Only admins can create categories"
        )

    existing = category_service.get_category_by_type(category_data.category_type)
    if existing:
        return ResponseFactory.conflict(
            message=f"Category '{category_data.category_type}' already exists"
        )

    new_category = category_service.create_category(category_data.category_type)
    return ResponseFactory.created(
        data=new_category,
        message="Category created successfully"
    )


@router.delete("/{category_id}")
def delete_category(
        category_id: int,
        category_service: CategoryService = Depends(get_category_service),
        current_user: User = Depends(get_current_user)
):
    """Удаление категории (только для админов)"""
    # ✅ Проверка прав
    if current_user.role != UserRole.ADMIN:
        return ResponseFactory.forbidden(
            message="Only admins can delete categories"
        )

    # ✅ Проверка существования
    category = category_service.get_category(category_id)
    if not category:
        return ResponseFactory.not_found(
            resource=f"Category with id {category_id}"
        )

    category_service.delete_category(category_id)
    return ResponseFactory.success(
        message="Category deleted successfully"
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(
        category_data: CategoryCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        category_service: CategoryService = Depends(get_category_service)
) :
    """Создание новой категории (только для админов)"""
    if current_user.role != UserRole.ADMIN :
        return ResponseFactory.forbidden(
            message="Only admins can create categories"
        )

    existing = category_service.get_category_by_type(db, category_data.category_type)
    if existing :
        return ResponseFactory.conflict(
            message=f"Category '{category_data.category_type}' already exists"
        )

    new_category = category_service.create_category(db, category_data.category_type)
    return ResponseFactory.created(
        data=CategoryResponse.model_validate(new_category, from_attributes=True).model_dump(),
        message="Category created successfully"
    )


@router.delete("/{category_id}")
def delete_category(
        category_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        category_service: CategoryService = Depends(get_category_service())
) :
    """Удаление категории (только для админов)"""
    # Проверка прав
    if current_user.role != UserRole.ADMIN :
        return ResponseFactory.forbidden(
            message="Only admins can delete categories"
        )

    # Проверка существования
    category = category_service.get_category(db, category_id)
    if not category :
        return ResponseFactory.not_found(
            resource=f"Category with id {category_id}"
        )

    category_service.delete_category(db, category_id)
    return ResponseFactory.success(
        message="Category deleted successfully"
    )