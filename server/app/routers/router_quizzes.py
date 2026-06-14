from typing import Optional

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session


from ..database.database import get_db
from ..models.model_user import User, UserRole
from ..schemas.schemas_response import ResponseFactory
from ..schemas.schemas_quiz import QuizResponse, QuizBase, QuizBulkCreate, QuizCreate, QuizUpdate, QuizBulkResponse
from ..utils.security import get_current_user, get_current_user_or_guest_optional
from ..services import QuizService


router = APIRouter(prefix="/quizzes", tags=["quizzes"])


def get_quiz_service(db: Session = Depends(get_db)) -> QuizService:
    """Ссылка на сервис"""
    return QuizService(db)


@router.post("", response_model=QuizBase, status_code=status.HTTP_201_CREATED)
def create_quiz(
        quiz: QuizCreate,
        quiz_service: QuizService = Depends(get_quiz_service),
        current_user: User = Depends(get_current_user)
):
    """Создание нового квиза"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can create quizzes directly")
    
    result = quiz_service.create_quiz(quiz, current_user.id, current_user.role)
    return result


@router.get("")
def get_quizzes(
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None,
        quiz_service: QuizService = Depends(get_quiz_service),
        current_user=Depends(get_current_user_or_guest_optional)
):
    """Получение списка квизов с учётом роли пользователя"""

    # Определяем, гость ли текущий пользователь
    is_guest = False
    if current_user and hasattr(current_user, 'session_id'):  # Это гость
        is_guest = True
    elif not current_user:
        # Неавторизованный пользователь тоже считается гостем
        is_guest = True

    quizzes = quiz_service.get_available_quizzes_for_user(
        is_guest=is_guest,
        skip=skip,
        limit=limit
    )

    if category_id:
        quizzes = [q for q in quizzes if q.get("category_id") == category_id]

    return ResponseFactory.success(
        data=quizzes,
        message="Quizzes retrieved successfully"
    )


@router.get("/categories")
def get_categories(quiz_service: QuizService = Depends(get_quiz_service)):
    """Получение всех категорий квизов"""
    return {"categories": quiz_service.get_quiz_categories()}


@router.get("/{quiz_id}")
def get_quiz(
        quiz_id: int,
        quiz_service: QuizService = Depends(get_quiz_service),
        current_user=Depends(get_current_user_or_guest_optional)
):
    """Получение конкретного квиза с проверкой доступа для гостей"""

    quiz = quiz_service.get_quiz(quiz_id)
    if not quiz:
        return ResponseFactory.not_found(f"Quiz {quiz_id}")

    # Определяем, гость ли пользователь
    is_guest = current_user and hasattr(current_user, 'session_id')

    # Проверка доступа для гостя
    if is_guest and not quiz_service.can_guest_access(quiz_id):
        return ResponseFactory.forbidden(
            message="Guests can only play single-player public quizzes"
        )

    # Проверка публичности для неавторизованных
    if not current_user and not quiz.get("is_public"):
        return ResponseFactory.unauthorized(
            message="Authentication required for this quiz"
        )

    return ResponseFactory.success(
        data=quiz,
        message="Quiz retrieved successfully"
    )


@router.get("/{quiz_id}/full")
def read_quiz_full(
        quiz_id: int,
        quiz_service: QuizService = Depends(get_quiz_service)
):
    """Получение полного квиза со всеми вопросами и ответами"""
    db_quiz = quiz_service.get_quiz_with_details(quiz_id)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz


@router.get("/{quiz_id}/edit")
def get_quiz_for_edit(
        quiz_id: int,
        quiz_service: QuizService = Depends(get_quiz_service),
        current_user: User = Depends(get_current_user)
):
    """Получение квиза в формате редактора (с вопросами и ответами)"""
    quiz = quiz_service.get_quiz_for_edit(quiz_id, current_user.id, current_user.role)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found or access denied")

    return ResponseFactory.success(
        data=quiz,
        message="Quiz editor data retrieved"
    )


@router.put("/{quiz_id}", response_model=QuizBase)
def update_quiz(
        quiz_id: int,
        quiz_update: QuizUpdate,
        quiz_service: QuizService = Depends(get_quiz_service),
        current_user: User = Depends(get_current_user)
):
    """Обновление квиза"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No admin access")
    
    db_quiz = quiz_service.update_quiz(quiz_id, quiz_update, current_user.id, current_user.role)

    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz


@router.delete("/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(
        quiz_id: int,
        quiz_service: QuizService = Depends(get_quiz_service),
        current_user: User = Depends(get_current_user)
):
    """Удаление квиза. Админ — любой квиз, автор — только свой."""
    is_admin = current_user.role == UserRole.ADMIN or current_user.role == "admin"
    deleted = quiz_service.delete_quiz(quiz_id, current_user.id, current_user.role)
    if not deleted:
        raise HTTPException(
            status_code=404, detail="Квиз не найден или недостаточно прав"
        )
    return


@router.get("/{quiz_id}/leaderboard")
def get_leaderboard(
        quiz_id: int,
        limit: int = 100,
        quiz_service: QuizService = Depends(get_quiz_service)
):
    """Получение таблицы лидеров для квиза"""
    leaderboard = quiz_service.get_quiz_leaderboard(quiz_id, limit)
    return ResponseFactory.success(data=leaderboard, message="Leaderboard retrieved")


@router.post("/bulk", response_model=QuizBulkResponse, status_code=status.HTTP_201_CREATED)
def create_quiz_bulk(
        quiz_data: QuizBulkCreate,
        quiz_service: QuizService = Depends(get_quiz_service),
        current_user: User = Depends(get_current_user)
):
    """Массовое создание квиза. Админ публикует сразу, обычный пользователь отправляет на модерацию."""
    result = quiz_service.create_quiz_bulk(quiz_data, current_user.id, current_user.role)
    result["status"] = "approved" if current_user.role == UserRole.ADMIN else "pending"
    return result


@router.put("/{quiz_id}/bulk")
def update_quiz_bulk(
        quiz_id: int,
        quiz_data: QuizBulkCreate,
        quiz_service: QuizService = Depends(get_quiz_service),
        current_user: User = Depends(get_current_user)
):
    """Полное обновление квиза с вопросами. Сбрасывает статус на pending для обычных пользователей."""
    result = quiz_service.update_quiz_bulk(quiz_id, quiz_data, current_user.id, current_user.role)
    if not result:
        raise HTTPException(status_code=404, detail="Quiz not found or access denied")
    return ResponseFactory.success(data=result, message="Quiz updated successfully")


@router.post("/pending")
def create_quiz_pending(
        quiz: QuizCreate,
        quiz_service: QuizService = Depends(get_quiz_service),
        current_user: User = Depends(get_current_user)
):
    """Создание квиза (отправляется на модерацию)"""
    if current_user.role == "guest":
        return ResponseFactory.forbidden("Guests cannot create quizzes")

    # Квиз отправляется на модерацию
    result = quiz_service.create_quiz_pending(quiz, current_user.id)

    return ResponseFactory.created(
        data=result,
        message="Quiz submitted for moderation"
    )
