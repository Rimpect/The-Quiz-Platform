from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..crud import crud_quiz as quiz_crud
from ..database.database import get_db
from ..models.model_user import User, UserRole
from ..models.model_pending_quiz import PendingQuizStatus
from ..schemas.schemas_response import ResponseFactory
from ..schemas.schemas_quiz import QuizResponse
from ..schemas.schemas_pending_quiz_response import PendingQuizResponse
from ..utils.security import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


def check_admin(current_user: User) :
    """Проверка прав администратора"""
    if current_user.role != UserRole.ADMIN :
        raise HTTPException(status_code=403, detail="Admin access required")


@router.get("/quizzes")
def get_all_quizzes(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) :
    """Получение списка всех опубликованных квизов (только админ)"""
    check_admin(current_user)

    quizzes = quiz_crud.get_quizzes(db, skip=skip, limit=limit, is_public=True)

    return ResponseFactory.success(
        data=[QuizResponse.model_validate(q).model_dump() for q in quizzes],
        message=f"Found {len(quizzes)} quizzes"
    )


@router.delete("/quizzes/{quiz_id}")
def delete_any_quiz(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) :
    """Удаление любого опубликованного квиза (только админ)"""
    check_admin(current_user)

    deleted = quiz_crud.delete_quiz(db, quiz_id, current_user.id, is_admin=True)
    if not deleted :
        return ResponseFactory.not_found(f"Quiz {quiz_id}")

    return ResponseFactory.success(message="Quiz deleted successfully")


@router.get("/pending")
def get_pending_quizzes(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) :
    """Получение списка квизов на модерации (только админ)"""
    check_admin(current_user)

    pending = quiz_crud.get_pending_quizzes(db, skip=skip, limit=limit, status=PendingQuizStatus.PENDING)

    return ResponseFactory.success(
        data=[{
            "id" : p.id,
            "title" : p.title,
            "category_id" : p.category_id,
            "description" : p.description,
            "cover_url" : p.cover_url,
            "quiz_mode" : p.quiz_mode,
            "author_id" : p.author_id,
            "created_at" : p.created_at.isoformat() if p.created_at else None
        } for p in pending],
        message=f"Found {len(pending)} pending quizzes"
    )


@router.post("/pending/{pending_id}/approve")
def approve_quiz(
        pending_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) :
    """Одобрение квиза (перенос в опубликованные)"""
    check_admin(current_user)

    approved_quiz = quiz_crud.approve_pending_quiz(db, pending_id, current_user.id)
    if not approved_quiz :
        return ResponseFactory.not_found(f"Pending quiz {pending_id}")

    return ResponseFactory.success(
        data=QuizResponse.model_validate(approved_quiz).model_dump(),
        message="Quiz approved and published"
    )


@router.delete("/pending/{pending_id}")
def reject_pending_quiz(
        pending_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) :
    """Отклонение квиза (удаление из модерации)"""
    check_admin(current_user)

    rejected = quiz_crud.reject_pending_quiz(db, pending_id, current_user.id)
    if not rejected :
        return ResponseFactory.not_found(f"Pending quiz {pending_id}")

    return ResponseFactory.success(message="Quiz rejected and removed")