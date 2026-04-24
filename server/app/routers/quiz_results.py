from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db
from app.utils.security import get_current_user

router = APIRouter(prefix="/quiz-results", tags=["quiz_results"])


@router.post("/", response_model=schemas.QuizResult, status_code=status.HTTP_201_CREATED)
def start_quiz(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
) :
    """Начало прохождения квиза"""
    # Проверяем существование квиза
    if not crud.get_quiz(db, quiz_id) :
        raise HTTPException(status_code=404, detail="Quiz not found")
    return crud.create_quiz_result(db, current_user.id, quiz_id)


@router.get("/me", response_model=List[schemas.QuizResult])
def get_my_results(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
) :
    """Получение всех результатов текущего пользователя"""
    return crud.get_user_quiz_results(db, current_user.id, skip, limit)


@router.get("/{result_id}", response_model=schemas.QuizResult)
def get_quiz_result(
        result_id: int,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
) :
    """Получение результата по ID"""
    result = crud.get_quiz_result(db, result_id)
    if not result or result.user_id != current_user.id :
        raise HTTPException(status_code=404, detail="Result not found")
    return result


@router.post("/{result_id}/answer")
def submit_answer(
        result_id: int,
        answer_data: schemas.UserAnswerCreate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
) :
    """Сохранение ответа пользователя"""
    result = crud.get_quiz_result(db, result_id)
    if not result or result.user_id != current_user.id :
        raise HTTPException(status_code=404, detail="Result not found")

    if result.is_completed :
        raise HTTPException(status_code=400, detail="Quiz already completed")

    return crud.save_user_answer(
        db,
        result_id,
        answer_data.question_id,
        answer_data.answer_text,
        answer_data.answer_id,
        answer_data.time_spent_seconds
    )


@router.post("/{result_id}/complete", response_model=schemas.QuizResult)
def complete_quiz(
        result_id: int,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
) :
    """Завершение квиза"""
    result = crud.get_quiz_result(db, result_id)
    if not result or result.user_id != current_user.id :
        raise HTTPException(status_code=404, detail="Result not found")

    if result.is_completed :
        raise HTTPException(status_code=400, detail="Quiz already completed")

    return crud.complete_quiz_result(db, result_id)


@router.get("/quiz/{quiz_id}/leaderboard")
def get_quiz_leaderboard(
        quiz_id: int,
        limit: int = 10,
        db: Session = Depends(get_db)
) :
    """Таблица лидеров для квиза"""
    if not crud.get_quiz(db, quiz_id) :
        raise HTTPException(status_code=404, detail="Quiz not found")
    return crud.get_quiz_leaderboard(db, quiz_id, limit)