from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models.model_user import User
from ..schemas.schemas_quiz import CategoryCreate
from ..schemas.schemas_response import ResponseFactory
from ..services import category_service
from ..utils.security import get_current_user

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("")
def get_all_categories(db: Session = Depends(get_db)):
    """Получение списка всех категорий (доступно всем)"""
    data = category_service.get_all_categories(db)
    return ResponseFactory.success(data=data, message="Categories retrieved successfully")


@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(
        category_data: CategoryCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """Создание новой категории (только для админов)"""
    data = category_service.create_category(db, category_data, current_user)
    return ResponseFactory.created(data=data, message="Category created successfully")


@router.delete("/{category_id}")
def delete_category(
        category_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """Удаление категории (только для админов)"""
    category_service.delete_category(db, category_id, current_user)
    return ResponseFactory.success(message="Category deleted successfully")
