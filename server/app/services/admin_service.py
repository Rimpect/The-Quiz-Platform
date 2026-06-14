"""Бизнес-логика админ-панели: модерация квизов (HTTP-агностична)."""
from sqlalchemy.orm import Session

from ..crud import crud_quiz as quiz_crud
from ..models.model_user import User, UserRole
from ..models.model_quiz import Quiz
from .exceptions import ForbiddenError, NotFoundError


def _ensure_admin(current_user: User):
    if current_user.role != UserRole.ADMIN:
        raise ForbiddenError("Admin access required")


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


def get_quizzes_by_status(db: Session, current_user: User, quiz_status: str, skip: int = 0, limit: int = 100):
    _ensure_admin(current_user)
    quizzes = quiz_crud.get_quizzes_by_status(db, quiz_status, skip, limit)
    return [_quiz_to_dict(q) for q in quizzes]


def approve_quiz(db: Session, current_user: User, quiz_id: int):
    _ensure_admin(current_user)
    quiz = quiz_crud.approve_quiz(db, quiz_id, current_user.id)
    if not quiz:
        raise NotFoundError(f"Quiz {quiz_id}")
    return _quiz_to_dict(quiz)


def reject_quiz(db: Session, current_user: User, quiz_id: int):
    _ensure_admin(current_user)
    quiz = quiz_crud.reject_quiz(db, quiz_id, current_user.id)
    if not quiz:
        raise NotFoundError(f"Quiz {quiz_id}")
    return _quiz_to_dict(quiz)


def delete_any_quiz(db: Session, current_user: User, quiz_id: int):
    _ensure_admin(current_user)
    deleted = quiz_crud.delete_quiz(db, quiz_id, current_user.id, is_admin=True)
    if not deleted:
        raise NotFoundError(f"Quiz {quiz_id}")
