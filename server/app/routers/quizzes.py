from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app import crud, schemas
from app.database import get_db
from app.utils.security import get_current_user

router = APIRouter(prefix="/quizzes", tags=["quizzes"])

@router.post("/", response_model=schemas.Quiz, status_code=status.HTTP_201_CREATED)
def create_quiz(
    quiz: schemas.QuizCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Создание нового квиза"""
    return crud.create_quiz(db=db, quiz=quiz)

@router.get("/", response_model=List[schemas.Quiz])
def read_quizzes(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    public_only: bool = Query(True, description="Только публичные квизы"),
    db: Session = Depends(get_db)
):
    """Получение списка квизов"""
    is_public = True if public_only else None
    return crud.get_quizzes(db, skip=skip, limit=limit, category=category, is_public=is_public)

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """Получение всех категорий квизов"""
    return {"categories": crud.get_quiz_categories(db)}

@router.get("/{quiz_id}", response_model=schemas.Quiz)
def read_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """Получение квиза по ID"""
    db_quiz = crud.get_quiz(db, quiz_id)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz

@router.get("/{quiz_id}/full")
def read_quiz_full(quiz_id: int, db: Session = Depends(get_db)):
    """Получение полного квиза со всеми вопросами и ответами"""
    db_quiz = crud.get_quiz_with_details(db, quiz_id)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz

@router.put("/{quiz_id}", response_model=schemas.Quiz)
def update_quiz(
    quiz_id: int,
    quiz_update: schemas.QuizUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Обновление квиза"""
    db_quiz = crud.update_quiz(db, quiz_id, quiz_update)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz

@router.delete("/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Удаление квиза"""
    if not crud.delete_quiz(db, quiz_id):
        raise HTTPException(status_code=404, detail="Quiz not found")

@router.get("/{quiz_id}/leaderboard")
def get_leaderboard(
    quiz_id: int,
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Получение таблицы лидеров для квиза"""
    # Проверяем существование квиза
    if not crud.get_quiz(db, quiz_id):
        raise HTTPException(status_code=404, detail="Quiz not found")
    return crud.get_quiz_leaderboard(db, quiz_id, limit)