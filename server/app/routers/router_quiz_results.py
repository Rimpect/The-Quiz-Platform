from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload
from typing import List

from ..crud import crud_quiz as crud_quiz, crud_quiz_result as crud_quiz_results, crud_achievement as crud_achievement
from ..database.database import get_db
from ..models import User
from ..models.model_quiz_result import QuizResult
from ..schemas.schemas_quiz_result import QuizResultBase
from ..schemas.schemas_response import ResponseFactory
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
    if not crud_quiz.get_quiz(db, body.quiz_id):
        raise HTTPException(status_code=404, detail="Quiz not found")

    completed_at = datetime.utcnow()
    started_at = completed_at - timedelta(seconds=max(body.duration_seconds, 0))

    result = QuizResult(
        user_id=current_user.id,
        quiz_id=body.quiz_id,
        score=body.score,
        max_score=body.max_score,
        is_completed=True,
        started_at=started_at,
        completed_at=completed_at,
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    newly_unlocked = crud_achievement.check_and_unlock_achievements(db, current_user.id)

    return ResponseFactory.success(
        data={"result_id": result.id, "newly_unlocked": newly_unlocked},
        message="Quiz result saved"
    )


@router.post("", response_model=QuizResultBase, status_code=status.HTTP_201_CREATED)
def start_quiz(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Сохранение игры квиза"""
    if not crud_quiz.get_quiz(db, quiz_id):
        raise HTTPException(status_code=404, detail="Quiz not found")
    return crud_quiz_results.create_quiz_result(db, current_user.id, quiz_id)


@router.get("/me", response_model=List[QuizResultBase])
def get_my_results(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получение всех результатов текущего пользователя"""
    return crud_quiz_results.get_user_quiz_results(db, current_user.id, skip, limit)


@router.get("/me/history")
def get_my_history(
        skip: int = 0,
        limit: int = 50,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """История квизов с названиями и категориями"""
    results = (
        db.query(QuizResult)
        .options(joinedload(QuizResult.quiz))
        .filter(QuizResult.user_id == current_user.id, QuizResult.is_completed == True)
        .order_by(QuizResult.completed_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    history = []
    for r in results:
        quiz = r.quiz
        history.append({
            "id": r.id,
            "quiz_id": r.quiz_id,
            "title": quiz.title if quiz else f"Квиз #{r.quiz_id}",
            "category": (quiz.category_ref.category_type if quiz and quiz.category_ref else ""),
            "score": r.score,
            "max_score": r.max_score,
            "percentage": round(r.percentage, 1),
            "total_questions": quiz.total_questions if quiz else 0,
            "completed_at": r.completed_at.isoformat() if r.completed_at else None,
            "duration_seconds": r.duration_seconds,
        })

    from ..schemas.schemas_response import ResponseFactory
    return ResponseFactory.success(data=history, message="History retrieved")


@router.get("/{result_id}", response_model=QuizResultBase)
def get_quiz_result(
        result_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получение результата по ID"""
    result = crud_quiz_results.get_quiz_result(db, result_id)
    if not result or result.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Result not found")
    if current_user.role != "admin":
        raise HTTPException(status_code=400, detail="No admin rules")
    return result


@router.post("/{result_id}/complete", response_model=QuizResultBase)
def complete_quiz(
        result_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Завершение квиза"""
    result = crud_quiz_results.get_quiz_result(db, result_id)
    if not result or result.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Result not found")

    if result.is_completed:
        raise HTTPException(status_code=400, detail="Quiz already completed")

    completed = crud_quiz_results.complete_quiz_result(db, result_id)

    # Автопроверка достижений после завершения квиза
    try:
        crud_achievement.check_and_unlock_achievements(db, current_user.id)
    except Exception:
        pass  # Не ломаем ответ если что-то пошло не так

    return completed


# "@router.get(")/quiz/{quiz_id}/leaderboard")
# def get_quiz_leaderboard(
#         quiz_id: int,
#         limit: int = 10,
#         db: Session = Depends(get_db)
# ):
#     """Таблица лидеров для квиза"""
#     if not crud_quiz.get_quiz(db, quiz_id):
#         raise HTTPException(status_code=404, detail="Quiz not found")
#     return crud_quiz_results.get_quiz_leaderboard(db, quiz_id, limit)
