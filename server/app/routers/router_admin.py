from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models.model_user import User, UserRole
from ..schemas.schemas_response import ResponseFactory
from ..utils.security import get_current_user
from ..services.service_quiz import QuizService

router = APIRouter(prefix="/admin", tags=["admin"])


def get_quiz_service(db: Session = Depends(get_db)) -> QuizService:
    """Dependency для получения экземпляра QuizService"""
    return QuizService(db)


def check_admin(current_user: User):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")


@router.get("/pending")
def get_pending_quizzes(
        skip: int = 0,
        limit: int = 100,
        quiz_service: QuizService = Depends(get_quiz_service),
        current_user: User = Depends(get_current_user)
):
    """Квизы на модерации (status='pending')"""
    check_admin(current_user)
    quizzes = quiz_service.get_pending_quizzes(skip=skip, limit=limit)
    return ResponseFactory.success(
        data=quizzes,
        message=f"Found {len(quizzes)} pending quizzes"
    )


@router.get("/rejected")
def get_rejected_quizzes(
        skip: int = 0,
        limit: int = 100,
        quiz_service: QuizService = Depends(get_quiz_service),
        current_user: User = Depends(get_current_user)
):
    """Отклонённые квизы"""
    check_admin(current_user)
    # Упрощено - в реальности нужен отдельный метод для rejected
    quizzes = []
    return ResponseFactory.success(
        data=quizzes,
        message=f"Found {len(quizzes)} rejected quizzes"
    )


@router.get("/quizzes")
def get_all_quizzes(
        skip: int = 0,
        limit: int = 100,
        quiz_service: QuizService = Depends(get_quiz_service),
        current_user: User = Depends(get_current_user)
):
    """Все опубликованные квизы (для AdminPanel)"""
    check_admin(current_user)
    quizzes = quiz_service.get_quizzes(skip=skip, limit=limit)
    return ResponseFactory.success(
        data=quizzes,
        message=f"Found {len(quizzes)} approved quizzes"
    )


@router.post("/quizzes/{quiz_id}/approve")
def approve_quiz(
        quiz_id: int,
        quiz_service: QuizService = Depends(get_quiz_service),
        current_user: User = Depends(get_current_user)
):
    """Одобрить квиз"""
    check_admin(current_user)
    quiz = quiz_service.approve_quiz(quiz_id, current_user.id)
    if not quiz:
        return ResponseFactory.not_found(f"Quiz {quiz_id}")
    return ResponseFactory.success(
        data=quiz,
        message="Quiz approved and published"
    )


@router.post("/quizzes/{quiz_id}/reject")
def reject_quiz(
        quiz_id: int,
        quiz_service: QuizService = Depends(get_quiz_service),
        current_user: User = Depends(get_current_user)
):
    """Отклонить квиз"""
    check_admin(current_user)
    result = quiz_service.reject_quiz(quiz_id, current_user.id)
    if not result:
        return ResponseFactory.not_found(f"Quiz {quiz_id}")
    return ResponseFactory.success(
        data={"quiz_id": quiz_id},
        message="Quiz rejected"
    )


@router.delete("/quizzes/{quiz_id}")
def delete_any_quiz(
        quiz_id: int,
        quiz_service: QuizService = Depends(get_quiz_service),
        current_user: User = Depends(get_current_user)
):
    """Удалить любой квиз"""
    check_admin(current_user)
    deleted = quiz_service.delete_quiz(quiz_id, current_user.id, current_user.role)
    if not deleted:
        return ResponseFactory.not_found(f"Quiz {quiz_id}")
    return ResponseFactory.success(message="Quiz deleted successfully")
