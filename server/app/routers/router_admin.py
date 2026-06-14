from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models.model_user import User
from ..schemas.schemas_response import ResponseFactory
from ..services import admin_service
from ..utils.security import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/pending")
def get_pending_quizzes(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Квизы на модерации (status='pending')"""
    data = admin_service.get_quizzes_by_status(db, current_user, "pending", skip, limit)
    return ResponseFactory.success(data=data, message=f"Found {len(data)} pending quizzes")


@router.get("/rejected")
def get_rejected_quizzes(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Отклонённые квизы"""
    data = admin_service.get_quizzes_by_status(db, current_user, "rejected", skip, limit)
    return ResponseFactory.success(data=data, message=f"Found {len(data)} rejected quizzes")


@router.get("/quizzes")
def get_all_quizzes(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Все опубликованные квизы (для AdminPanel)"""
    data = admin_service.get_quizzes_by_status(db, current_user, "approved", skip, limit)
    return ResponseFactory.success(data=data, message=f"Found {len(data)} approved quizzes")


@router.post("/quizzes/{quiz_id}/approve")
def approve_quiz(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Одобрить квиз"""
    data = admin_service.approve_quiz(db, current_user, quiz_id)
    return ResponseFactory.success(data=data, message="Quiz approved and published")


@router.post("/quizzes/{quiz_id}/reject")
def reject_quiz(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Отклонить квиз"""
    data = admin_service.reject_quiz(db, current_user, quiz_id)
    return ResponseFactory.success(data=data, message="Quiz rejected")


@router.delete("/quizzes/{quiz_id}")
def delete_any_quiz(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Удалить любой квиз"""
    admin_service.delete_any_quiz(db, current_user, quiz_id)
    return ResponseFactory.success(message="Quiz deleted successfully")
