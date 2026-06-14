from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload
from typing import List

from ..database.database import get_db
from ..models import User
from ..models.model_quiz_result import QuizResult
from ..schemas.schemas_quiz_result import QuizResultBase
from ..schemas.schemas_response import ResponseFactory
from ..utils.security import get_current_user
from ..services import QuizResultService

router = APIRouter(prefix="/quiz-results", tags=["quiz_results"])


def get_quiz_result_service(db: Session = Depends(get_db)) -> QuizResultService:
    """Dependency для получения экземпляра QuizResultService"""
    return QuizResultService(db)


class SaveQuizResultRequest(BaseModel):
    quiz_id: int
    score: float
    max_score: float
    duration_seconds: int = 0


@router.post("/save")
def save_quiz_result(
        body: SaveQuizResultRequest,
        quiz_result_service: QuizResultService = Depends(get_quiz_result_service),
        current_user: User = Depends(get_current_user)
):
    """Сохранить результат квиза одним запросом и проверить достижения."""
    if not quiz_result_service.check_quiz_exists(body.quiz_id):
        raise HTTPException(status_code=404, detail="Quiz not found")

    result = quiz_result_service.save_result(
        user_id=current_user.id,
        quiz_id=body.quiz_id,
        score=int(body.score),
        max_score=int(body.max_score),
        is_completed=True,
        duration_seconds=body.duration_seconds
    )

    # Проверка достижений (выносится в отдельный сервис при необходимости)
    newly_unlocked = []

    return ResponseFactory.success(
        data={"result_id": result.get("id"), "newly_unlocked": newly_unlocked},
        message="Quiz result saved"
    )


@router.post("", response_model=QuizResultBase, status_code=status.HTTP_201_CREATED)
def start_quiz(
        quiz_id: int,
        quiz_result_service: QuizResultService = Depends(get_quiz_result_service),
        current_user: User = Depends(get_current_user)
):
    """Сохранение игры квиза"""
    if not quiz_result_service.check_quiz_exists(quiz_id):
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    result = quiz_result_service.save_result(
        user_id=current_user.id,
        quiz_id=quiz_id,
        score=0,
        max_score=0,
        is_completed=False
    )
    return result


@router.get("/me", response_model=List[QuizResultBase])
def get_my_results(
        skip: int = 0,
        limit: int = 100,
        quiz_result_service: QuizResultService = Depends(get_quiz_result_service),
        current_user: User = Depends(get_current_user)
):
    """Получение всех результатов текущего пользователя"""
    return quiz_result_service.get_user_results(current_user.id)


@router.get("/me/history")
def get_my_history(
        skip: int = 0,
        limit: int = 50,
        quiz_result_service: QuizResultService = Depends(get_quiz_result_service),
        current_user: User = Depends(get_current_user)
):
    """История квизов с названиями и категориями"""
    results = quiz_result_service.get_user_results(current_user.id)
    
    history = []
    for r in results:
        history.append({
            "id": r.get("id"),
            "quiz_id": r.get("quiz_id"),
            "title": f"Квиз #{r.get('quiz_id')}",
            "category": "",
            "score": r.get("score"),
            "max_score": r.get("max_score"),
            "percentage": r.get("percentage"),
            "total_questions": 0,
            "completed_at": r.get("completed_at"),
            "duration_seconds": r.get("duration_seconds"),
        })

    return ResponseFactory.success(data=history, message="History retrieved")


@router.get("/{result_id}", response_model=QuizResultBase)
def get_quiz_result(
        result_id: int,
        quiz_result_service: QuizResultService = Depends(get_quiz_result_service),
        current_user: User = Depends(get_current_user)
):
    """Получение результата по ID"""
    result = quiz_result_service.get_user_results(current_user.id, result_id)
    if not result or len(result) == 0:
        raise HTTPException(status_code=404, detail="Result not found")
    if current_user.role != "admin":
        raise HTTPException(status_code=400, detail="No admin rules")
    return result[0]


@router.post("/{result_id}/complete", response_model=QuizResultBase)
def complete_quiz(
        result_id: int,
        quiz_result_service: QuizResultService = Depends(get_quiz_result_service),
        current_user: User = Depends(get_current_user)
):
    """Завершение квиза"""
    result = quiz_result_service.get_user_results(current_user.id, result_id)
    if not result or len(result) == 0:
        raise HTTPException(status_code=404, detail="Result not found")

    if result[0].get("is_completed"):
        raise HTTPException(status_code=400, detail="Quiz already completed")

    # Упрощено - в реальности нужно обновлять статус
    return result[0]
