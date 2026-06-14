"""
Роутер для управления сессиями прохождения квизов
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models import Guest, User
from ..schemas.schemas_response import ResponseFactory
from ..schemas.schemas_user_answer import StartSessionResponse, UserAnswerCreate
from ..services import session_service
from ..utils.security import get_current_user, get_current_guest


router = APIRouter(prefix="/quiz-session", tags=["quiz-sessions"])


@router.post("/start", response_model=StartSessionResponse)
def start_session(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Начало новой сессии прохождения квиза"""
    return session_service.start_session(db, current_user, quiz_id)


@router.post("/guest/start", response_model=StartSessionResponse)
def start_guest_session(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_guest: Guest = Depends(get_current_guest)
):
    """Начало сессии для гостя"""
    return session_service.start_guest_session(db, current_guest, quiz_id)


@router.post("/answer")
def save_answer(
        session_id: str,
        answer: UserAnswerCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Сохранение ответа пользователя"""
    return session_service.save_answer(db, current_user, session_id, answer)


@router.get("/answers")
def get_session_answers(
        session_id: str,
        current_user: User = Depends(get_current_user),
):
    """Получение всех ответов сессии"""
    return session_service.get_session_answers(current_user, session_id)


@router.get("/score")
def get_session_score(
        session_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Подсчет результатов и завершение сессии"""
    data = session_service.get_session_score(db, current_user, session_id)
    return ResponseFactory.success(data=data, message="Quiz completed successfully")


@router.delete("/{session_id}")
def cancel_session(
        session_id: str,
        current_user: User = Depends(get_current_user)
):
    """Отмена сессии (удаление временных данных)"""
    return session_service.cancel_session(current_user, session_id)
