from typing import Optional

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session


from ..crud import crud_quiz as crud_quiz
from ..database.database import get_db
from ..models.model_user import User, UserRole
from ..schemas.schemas_response import ResponseFactory
from ..schemas.schemas_quiz import QuizResponse, QuizBase, QuizBulkCreate, QuizBulkResponse, QuizCreate, QuizUpdate
from ..utils.security import get_current_user, get_current_user_or_guest_optional


router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.post("/", response_model=QuizBase, status_code=status.HTTP_201_CREATED)
def create_quiz(
        quiz: QuizCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Создание нового квиза"""
    if current_user.role == UserRole.ADMIN:
        return crud_quiz.create_quiz_fast(db=db, quiz=quiz, author_id=current_user.id)
    raise HTTPException(status_code=404, detail="Quiz not found")


@router.get("/")
def get_quizzes(
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None,
        db: Session = Depends(get_db),
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

    quizzes = crud_quiz.get_available_quizzes_for_user(
        db,
        is_guest=is_guest,
        skip=skip,
        limit=limit
    )

    if category_id:
        quizzes = [q for q in quizzes if q.category_id == category_id]

    return ResponseFactory.success(
        data=[QuizResponse.model_validate(q) for q in quizzes],
        message="Quizzes retrieved successfully"
    )


@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """Получение всех категорий квизов"""
    return {"categories": crud_quiz.get_quiz_categories(db)}


@router.get("/{quiz_id}")
def get_quiz(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user_or_guest_optional)
):
    """Получение конкретного квиза с проверкой доступа для гостей"""

    quiz = crud_quiz.get_quiz(db, quiz_id)
    if not quiz:
        return ResponseFactory.not_found(f"Quiz {quiz_id}")

    # Определяем, гость ли пользователь
    is_guest = current_user and hasattr(current_user, 'session_id')

    # Проверка доступа для гостя
    if is_guest and not crud_quiz.can_guest_access_quiz(db, quiz_id):
        return ResponseFactory.forbidden(
            message="Guests can only play single-player public quizzes"
        )

    # Проверка публичности для неавторизованных
    if not current_user and not quiz.is_public:
        return ResponseFactory.unauthorized(
            message="Authentication required for this quiz"
        )

    return ResponseFactory.success(
        data=QuizResponse.model_validate(quiz),
        message="Quiz retrieved successfully"
    )


@router.get("/{quiz_id}/full")
def read_quiz_full(quiz_id: int, db: Session = Depends(get_db)):
    """Получение полного квиза со всеми вопросами и ответами"""
    db_quiz = crud_quiz.get_quiz_with_details(db, quiz_id)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz


@router.put("/{quiz_id}", response_model=QuizBase)
def update_quiz(
        quiz_id: int,
        quiz_update: QuizUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    quiz = crud_quiz.get_quiz(db, quiz_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    """Обновление квиза"""
    if current_user.role == UserRole.ADMIN or quiz.author_id == current_user.id:
        db_quiz = crud_quiz.update_quiz(db, quiz_id, quiz_update, current_user.id)

        if db_quiz is None:
            raise HTTPException(status_code=404, detail="Quiz not found")
        return db_quiz

    raise HTTPException(status_code=404, detail="No rights")


@router.delete("/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    quiz = crud_quiz.get_quiz(db, quiz_id)
    if quiz is None :
        raise HTTPException(status_code=404, detail="Quiz not found")
    """Удаление квиза"""
    if current_user.role == UserRole.ADMIN or quiz.author_id == current_user.id:
        if not crud_quiz.delete_quiz(db, quiz_id, current_user.id):
            raise HTTPException(status_code=404, detail="Quiz not found")
    raise HTTPException(status_code=403, detail="Not rights")


"""@router.get("/{quiz_id}/leaderboard")
def get_leaderboard(
        quiz_id: int,
        limit: int = Query(10, ge=1, le=100),
        db: Session = Depends(get_db)
):
    "Получение таблицы лидеров для квиза"
    # Проверяем существование квиза
    if not crud_quiz.get_quiz(db, quiz_id):
        raise HTTPException(status_code=404, detail="Quiz not found")
    return crud_quiz.get_quiz_leaderboard(db, quiz_id, limit)
"""


@router.post("/bulk", response_model=QuizBulkResponse, status_code=status.HTTP_201_CREATED)
def create_quiz_bulk(
        quiz_data: QuizBulkCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Массовое создание квиза с вопросами и ответами за один запрос
    """
    if current_user.role == UserRole.ADMIN:
        result = crud_quiz.create_quiz_full(db, quiz_data, current_user.id)
        return result
    raise HTTPException(status_code=404, detail="No admin or author rules")


@router.post("/pending")
def create_quiz(
        quiz: QuizCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Создание квиза (отправляется на модерацию)"""
    if current_user.role == "guest":
        return ResponseFactory.forbidden("Guests cannot create quizzes")

    # Квиз отправляется на модерацию
    pending = crud_quiz.create_quiz_pending(db, quiz, current_user.id)

    return ResponseFactory.created(
        data={
            "id": pending.id,
            "title": pending.title,
            "status": "pending",
            "message": "Your quiz has been submitted for moderation"
        },
        message="Quiz submitted for moderation"
    )
