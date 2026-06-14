"""Бизнес-логика квизов (HTTP-агностична: данные + доменные исключения)."""
from typing import Optional

from sqlalchemy.orm import Session

from ..crud import crud_quiz
from ..models.model_user import User, UserRole
from ..schemas.schemas_quiz import QuizResponse, QuizCreate, QuizUpdate, QuizBulkCreate
from .exceptions import NotFoundError, ForbiddenError, UnauthorizedError


def _is_guest(current_user) -> bool:
    """Гость — это либо guest-сессия, либо неавторизованный пользователь."""
    if current_user and hasattr(current_user, "session_id"):
        return True
    return not current_user


def create_quiz(db: Session, quiz: QuizCreate, current_user: User):
    if current_user.role == UserRole.ADMIN:
        return crud_quiz.create_quiz_fast(db=db, quiz=quiz, author_id=current_user.id)
    raise NotFoundError("Quiz not found")


def get_quizzes(
        db: Session,
        current_user,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None,
):
    quizzes = crud_quiz.get_available_quizzes_for_user(
        db, is_guest=_is_guest(current_user), skip=skip, limit=limit
    )
    if category_id:
        quizzes = [q for q in quizzes if q.category_id == category_id]
    return [QuizResponse.model_validate(q) for q in quizzes]


def get_quiz_categories(db: Session):
    return {"categories": crud_quiz.get_quiz_categories(db)}


def get_quiz(db: Session, quiz_id: int, current_user):
    quiz = crud_quiz.get_quiz(db, quiz_id)
    if not quiz:
        raise NotFoundError(f"Quiz {quiz_id}")

    is_guest = current_user and hasattr(current_user, "session_id")
    if is_guest and not crud_quiz.can_guest_access_quiz(db, quiz_id):
        raise ForbiddenError("Guests can only play single-player public quizzes")

    if not current_user and not quiz.is_public:
        raise UnauthorizedError("Authentication required for this quiz")

    return QuizResponse.model_validate(quiz)


def read_quiz_full(db: Session, quiz_id: int):
    db_quiz = crud_quiz.get_quiz_with_details(db, quiz_id)
    if db_quiz is None:
        raise NotFoundError("Quiz not found")
    return db_quiz


def get_quiz_for_edit(db: Session, quiz_id: int, current_user: User):
    quiz = crud_quiz.get_quiz_with_details(db, quiz_id)
    if not quiz:
        raise NotFoundError("Quiz not found")
    if quiz.author_id != current_user.id and current_user.role != "admin":
        raise ForbiddenError("Not your quiz")

    return {
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
    }


def update_quiz(db: Session, quiz_id: int, quiz_update: QuizUpdate, current_user: User):
    if current_user.role == "admin":
        db_quiz = crud_quiz.update_quiz(db, quiz_id, quiz_update)
        if db_quiz is None:
            raise NotFoundError("Quiz not found")
        return db_quiz

    raise NotFoundError("No admin or author rules")


def delete_quiz(db: Session, quiz_id: int, current_user: User):
    is_admin = current_user.role == UserRole.ADMIN or current_user.role == "admin"
    deleted = crud_quiz.delete_quiz(db, quiz_id, current_user.id, is_admin=is_admin)
    if not deleted:
        raise NotFoundError("Квиз не найден или недостаточно прав")


def get_leaderboard(db: Session, quiz_id: int, limit: int = 100):
    if not crud_quiz.get_quiz(db, quiz_id):
        raise NotFoundError("Quiz not found")
    return crud_quiz.get_quiz_leaderboard(db, quiz_id, limit)


def create_quiz_bulk(db: Session, quiz_data: QuizBulkCreate, current_user: User):
    quiz_status = "approved" if current_user.role == UserRole.ADMIN else "pending"
    result = crud_quiz.create_quiz_full(
        db, quiz_data, author_id=current_user.id, status=quiz_status
    )
    result["status"] = quiz_status
    return result


def update_quiz_bulk(db: Session, quiz_id: int, quiz_data: QuizBulkCreate, current_user: User):
    is_admin = current_user.role == UserRole.ADMIN
    result = crud_quiz.update_quiz_full(
        db, quiz_id, quiz_data, user_id=current_user.id, is_admin=is_admin
    )
    if not result:
        raise NotFoundError("Quiz not found or access denied")
    return result


def create_quiz_pending(db: Session, quiz: QuizCreate, current_user: User):
    if current_user.role == "guest":
        raise ForbiddenError("Guests cannot create quizzes")

    pending = crud_quiz.create_quiz_pending(db, quiz, current_user.id)
    return {
        "id": pending.id,
        "title": pending.title,
        "status": "pending",
        "message": "Your quiz has been submitted for moderation",
    }
