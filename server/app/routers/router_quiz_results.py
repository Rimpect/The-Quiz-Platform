from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

from ..database.database import get_db
from ..models import User
from ..schemas.schemas_quiz_result import QuizResultBase
from ..schemas.schemas_response import ResponseFactory
from ..services import quiz_result_service
from ..utils.security import get_current_user

router = APIRouter(prefix="/quiz-results", tags=["quiz_results"])


class SaveQuizResultRequest(BaseModel):
    quiz_id: int
    score: float
    max_score: float
    duration_seconds: int = 0


@router.post("/save")
def save_quiz_result(
        body: SaveQuizResultRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Сохранить результат квиза одним запросом и проверить достижения."""
    data = quiz_result_service.save_quiz_result(
        db, current_user, body.quiz_id, body.score, body.max_score, body.duration_seconds
    )
    return ResponseFactory.success(data=data, message="Quiz result saved")


@router.post("", response_model=QuizResultBase, status_code=status.HTTP_201_CREATED)
def start_quiz(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Сохранение игры квиза"""
    return quiz_result_service.start_quiz(db, current_user, quiz_id)


@router.get("/me", response_model=List[QuizResultBase])
def get_my_results(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получение всех результатов текущего пользователя"""
    return quiz_result_service.get_my_results(db, current_user, skip, limit)


@router.get("/me/history")
def get_my_history(
        skip: int = 0,
        limit: int = 50,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """История квизов с названиями и категориями"""
    history = quiz_result_service.get_my_history(db, current_user, skip, limit)
    return ResponseFactory.success(data=history, message="History retrieved")


@router.get("/{result_id}", response_model=QuizResultBase)
def get_quiz_result(
        result_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получение результата по ID"""
    return quiz_result_service.get_quiz_result(db, current_user, result_id)


@router.post("/{result_id}/complete", response_model=QuizResultBase)
def complete_quiz(
        result_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Завершение квиза"""
    return quiz_result_service.complete_quiz(db, current_user, result_id)
