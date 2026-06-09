from typing import Optional

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from ..crud import crud_quiz as crud_quiz
from ..database.database import get_db
from ..models.model_user import User
from ..schemas import ResponseFactory, QuizResponse
from ..utils.security import get_current_user, get_current_user_or_guest_optional

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.post("/", response_model=schemas.QuizBase, status_code=status.HTTP_201_CREATED)
def create_quiz(
        quiz: schemas.QuizCreate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    """Создание нового квиза"""
    if current_user.role in ("admin", "author"):
        return crud_quiz.create_quiz(db=db, quiz=quiz)
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


@router.put("/{quiz_id}", response_model=schemas.QuizBase)
def update_quiz(
        quiz_id: int,
        quiz_update: schemas.QuizUpdate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    """Обновление квиза"""
    if current_user.role == "admin":
        db_quiz = crud_quiz.update_quiz(db, quiz_id, quiz_update)

        if db_quiz is None:
            raise HTTPException(status_code=404, detail="Quiz not found")
        return db_quiz

    raise HTTPException(status_code=404, detail="No admin or author rules")


@router.delete("/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    """Удаление квиза"""
    if current_user.role == "admin":
        if not crud_quiz.delete_quiz(db, quiz_id):
            raise HTTPException(status_code=404, detail="Quiz not found")
    raise HTTPException(status_code=404, detail="No admin or author rules")


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


@router.post("/bulk", response_model=schemas.QuizBulkResponse, status_code=status.HTTP_201_CREATED)
def create_quiz_bulk(
        quiz_data: schemas.QuizBulkCreate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    """
    Массовое создание квиза с вопросами и ответами за один запрос

    Пример тела запроса:
    {
        "title": "Python Basics Quiz",
        "category": "Programming",
        "description": "Test your Python knowledge",
        "is_public": true,
        "quiz_mode": "single",
        "questions":
        [
            {
                "answer_type": "single",
                "points": 10,
                "question_text": "What is Python?",
                "time_limit_seconds": 30,
                "answers": [
                    {"answer_text": "A snake", "is_correct": false, "order_number": 1},
                    {"answer_text": "A programming language", "is_correct": true, "order_number": 2},
                    {"answer_text": "A car", "is_correct": false, "order_number": 3}
                ]
            },
            {
                "answer_type": "multiple",
                "points": 20,
                "question_text": "Which of these are Python frameworks?",
                "time_limit_seconds": 45,
                "answers": [
                    {"answer_text": "Django", "is_correct": true, "order_number": 1},
                    {"answer_text": "Flask", "is_correct": true, "order_number": 2},
                    {"answer_text": "React", "is_correct": false, "order_number": 3},
                    {"answer_text": "Spring", "is_correct": false, "order_number": 4}
                ]
            }
        ]
    }
    """
    if current_user.role in ("admin", "author"):
        result = crud_quiz.create_quiz_full(db, quiz_data)
        return result
    raise HTTPException(status_code=404, detail="No admin or author rules")


@router.post("/")
def create_quiz(
        quiz: schemas.QuizCreate,
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

