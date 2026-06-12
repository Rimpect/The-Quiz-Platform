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


@router.post("", response_model=QuizBase, status_code=status.HTTP_201_CREATED)
def create_quiz(
        quiz: QuizCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Создание нового квиза"""
    if current_user.role == UserRole.ADMIN:
        return crud_quiz.create_quiz_fast(db=db, quiz=quiz, author_id=current_user.id)
    raise HTTPException(status_code=404, detail="Quiz not found")


@router.get("")
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


@router.get("/{quiz_id}/edit")
def get_quiz_for_edit(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получение квиза в формате редактора (с вопросами и ответами)"""
    quiz = crud_quiz.get_quiz_with_details(db, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    if quiz.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not your quiz")

    return ResponseFactory.success(
        data={
            "id": quiz.id,
            "title": quiz.title,
            "description": quiz.description or "",
            "categoryId": str(quiz.category_id) if quiz.category_id else "",
            "difficulty": quiz.difficulty or "easy",
            "quizMode": quiz.quiz_mode or "single",
            "lobbyWaitTimeSeconds": quiz.lobby_wait_time_seconds or 30,
            "maxTeamMembers": quiz.max_team_members or 10,
            "coverUrl": quiz.cover_url or "",
            "status": quiz.status,
            "questions": [
                {
                    "id": q.id,
                    "questionText": q.question_text,
                    "questionType": getattr(q.answer_type, "value", q.answer_type) or "single",
                    "timeLimitSeconds": q.time_limit_seconds or 0,
                    "points": q.points or 10,
                    "mediaUrl": q.question_media_url or "",
                    "answers": [
                        {
                            "id": a.id,
                            "text": a.answer_text,
                            "isCorrect": a.is_correct,
                        }
                        for a in sorted(q.answers, key=lambda x: x.order_number)
                    ],
                }
                for q in quiz.questions
            ],
        },
        message="Quiz editor data retrieved"
    )


@router.put("/{quiz_id}", response_model=QuizBase)
def update_quiz(
        quiz_id: int,
        quiz_update: QuizUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
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
        current_user: User = Depends(get_current_user)
):
    """Удаление квиза. Админ — любой квиз, автор — только свой."""
    is_admin = current_user.role == UserRole.ADMIN or current_user.role == "admin"
    deleted = crud_quiz.delete_quiz(db, quiz_id, current_user.id, is_admin=is_admin)
    if not deleted:
        raise HTTPException(
            status_code=404, detail="Квиз не найден или недостаточно прав"
        )
    return


@router.get("/{quiz_id}/leaderboard")
def get_leaderboard(
        quiz_id: int,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    """Получение таблицы лидеров для квиза"""
    # Проверяем существование квиза
    if not crud_quiz.get_quiz(db, quiz_id):
        raise HTTPException(status_code=404, detail="Quiz not found")

    leaderboard = crud_quiz.get_quiz_leaderboard(db, quiz_id, limit)
    return ResponseFactory.success(data=leaderboard, message="Leaderboard retrieved")


@router.post("/bulk", response_model=QuizBulkResponse, status_code=status.HTTP_201_CREATED)
def create_quiz_bulk(
        quiz_data: QuizBulkCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Массовое создание квиза. Админ публикует сразу, обычный пользователь отправляет на модерацию."""
    quiz_status = "approved" if current_user.role == UserRole.ADMIN else "pending"
    result = crud_quiz.create_quiz_full(db, quiz_data, author_id=current_user.id, status=quiz_status)
    result["status"] = quiz_status
    return result


@router.put("/{quiz_id}/bulk")
def update_quiz_bulk(
        quiz_id: int,
        quiz_data: QuizBulkCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Полное обновление квиза с вопросами. Сбрасывает статус на pending для обычных пользователей."""
    is_admin = current_user.role == UserRole.ADMIN
    result = crud_quiz.update_quiz_full(db, quiz_id, quiz_data, user_id=current_user.id, is_admin=is_admin)
    if not result:
        raise HTTPException(status_code=404, detail="Quiz not found or access denied")
    return ResponseFactory.success(data=result, message="Quiz updated successfully")


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
