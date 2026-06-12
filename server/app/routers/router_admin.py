from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from ..crud import crud_quiz as quiz_crud
from ..database.database import get_db
from ..models.model_user import User, UserRole
from ..models.model_quiz import Quiz
from ..schemas.schemas_response import ResponseFactory
from ..schemas.schemas_quiz import QuizResponse
from ..utils.security import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


def check_admin(current_user: User):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")


def _quiz_to_dict(q: Quiz) -> dict:
    return {
        "id": q.id,
        "title": q.title,
        "description": q.description,
        "difficulty": q.difficulty,
        "quiz_mode": q.quiz_mode,
        "status": q.status,
        "is_public": q.is_public,
        "category": q.category_ref.category_type if q.category_ref else "",
        "category_id": q.category_id,
        "cover_url": q.cover_url,
        "author_id": q.author_id,
        "author": q.author.nickname if q.author else str(q.author_id),
        "total_questions": q.total_questions,
        "duration_minutes": q.duration_minutes,
        "created_at": q.created_at.isoformat() if q.created_at else None,
    }


@router.get("/pending")
def get_pending_quizzes(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Квизы на модерации (status='pending')"""
    check_admin(current_user)
    quizzes = quiz_crud.get_quizzes_by_status(db, "pending", skip, limit)
    return ResponseFactory.success(
        data=[_quiz_to_dict(q) for q in quizzes],
        message=f"Found {len(quizzes)} pending quizzes"
    )


@router.get("/rejected")
def get_rejected_quizzes(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Отклонённые квизы"""
    check_admin(current_user)
    quizzes = quiz_crud.get_quizzes_by_status(db, "rejected", skip, limit)
    return ResponseFactory.success(
        data=[_quiz_to_dict(q) for q in quizzes],
        message=f"Found {len(quizzes)} rejected quizzes"
    )


@router.get("/quizzes")
def get_all_quizzes(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Все опубликованные квизы (для AdminPanel)"""
    check_admin(current_user)
    quizzes = quiz_crud.get_quizzes_by_status(db, "approved", skip, limit)
    return ResponseFactory.success(
        data=[_quiz_to_dict(q) for q in quizzes],
        message=f"Found {len(quizzes)} approved quizzes"
    )


@router.post("/quizzes/{quiz_id}/approve")
def approve_quiz(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Одобрить квиз"""
    check_admin(current_user)
    quiz = quiz_crud.approve_quiz(db, quiz_id, current_user.id)
    if not quiz:
        return ResponseFactory.not_found(f"Quiz {quiz_id}")
    return ResponseFactory.success(
        data=_quiz_to_dict(quiz),
        message="Quiz approved and published"
    )


@router.post("/quizzes/{quiz_id}/reject")
def reject_quiz(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Отклонить квиз"""
    check_admin(current_user)
    quiz = quiz_crud.reject_quiz(db, quiz_id, current_user.id)
    if not quiz:
        return ResponseFactory.not_found(f"Quiz {quiz_id}")
    return ResponseFactory.success(
        data=_quiz_to_dict(quiz),
        message="Quiz rejected"
    )


@router.delete("/quizzes/{quiz_id}")
def delete_any_quiz(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Удалить любой квиз"""
    check_admin(current_user)
    deleted = quiz_crud.delete_quiz(db, quiz_id, current_user.id, is_admin=True)
    if not deleted:
        return ResponseFactory.not_found(f"Quiz {quiz_id}")
    return ResponseFactory.success(message="Quiz deleted successfully")
