from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models.model_user import User
from ..schemas.schemas_quiz import QuizBase, QuizBulkCreate, QuizBulkResponse, QuizCreate, QuizUpdate
from ..schemas.schemas_response import ResponseFactory
from ..services import quiz_service
from ..utils.security import get_current_user, get_current_user_or_guest_optional


router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.post("", response_model=QuizBase, status_code=status.HTTP_201_CREATED)
def create_quiz(
        quiz: QuizCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Создание нового квиза"""
    return quiz_service.create_quiz(db, quiz, current_user)


@router.get("")
def get_quizzes(
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user_or_guest_optional)
):
    """Получение списка квизов с учётом роли пользователя"""
    data = quiz_service.get_quizzes(db, current_user, skip=skip, limit=limit, category_id=category_id)
    return ResponseFactory.success(data=data, message="Quizzes retrieved successfully")


@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """Получение всех категорий квизов"""
    return quiz_service.get_quiz_categories(db)


@router.get("/{quiz_id}")
def get_quiz(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user_or_guest_optional)
):
    """Получение конкретного квиза с проверкой доступа для гостей"""
    data = quiz_service.get_quiz(db, quiz_id, current_user)
    return ResponseFactory.success(data=data, message="Quiz retrieved successfully")


@router.get("/{quiz_id}/full")
def read_quiz_full(quiz_id: int, db: Session = Depends(get_db)):
    """Получение полного квиза со всеми вопросами и ответами"""
    return quiz_service.read_quiz_full(db, quiz_id)


@router.get("/{quiz_id}/edit")
def get_quiz_for_edit(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получение квиза в формате редактора (с вопросами и ответами)"""
    data = quiz_service.get_quiz_for_edit(db, quiz_id, current_user)
    return ResponseFactory.success(data=data, message="Quiz editor data retrieved")


@router.put("/{quiz_id}", response_model=QuizBase)
def update_quiz(
        quiz_id: int,
        quiz_update: QuizUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Обновление квиза"""
    return quiz_service.update_quiz(db, quiz_id, quiz_update, current_user)


@router.delete("/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Удаление квиза. Админ — любой квиз, автор — только свой."""
    quiz_service.delete_quiz(db, quiz_id, current_user)


@router.get("/{quiz_id}/leaderboard")
def get_leaderboard(
        quiz_id: int,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    """Получение таблицы лидеров для квиза"""
    leaderboard = quiz_service.get_leaderboard(db, quiz_id, limit)
    return ResponseFactory.success(data=leaderboard, message="Leaderboard retrieved")


@router.post("/bulk", response_model=QuizBulkResponse, status_code=status.HTTP_201_CREATED)
def create_quiz_bulk(
        quiz_data: QuizBulkCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Массовое создание квиза. Админ публикует сразу, обычный пользователь отправляет на модерацию."""
    return quiz_service.create_quiz_bulk(db, quiz_data, current_user)


@router.put("/{quiz_id}/bulk")
def update_quiz_bulk(
        quiz_id: int,
        quiz_data: QuizBulkCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Полное обновление квиза с вопросами. Сбрасывает статус на pending для обычных пользователей."""
    result = quiz_service.update_quiz_bulk(db, quiz_id, quiz_data, current_user)
    return ResponseFactory.success(data=result, message="Quiz updated successfully")


@router.post("/pending")
def create_quiz_pending(
        quiz: QuizCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Создание квиза (отправляется на модерацию)"""
    data = quiz_service.create_quiz_pending(db, quiz, current_user)
    return ResponseFactory.created(data=data, message="Quiz submitted for moderation")
