from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..crud import crud_quiz as crud_quiz
from .. import schemas
from ..database.database import get_db
from ..utils.security import get_current_user

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.post("/", response_model=schemas.QuizBase, status_code=status.HTTP_201_CREATED)
def create_quiz(
        quiz: schemas.QuizCreate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
) :
    """Создание нового квиза"""
    return crud_quiz.create_quiz(db=db, quiz=quiz)


@router.get("/", response_model=List[schemas.QuizBase])
def read_quizzes(
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = Query(None, description="Фильтр по категории"),
        public_only: bool = Query(True, description="Только публичные квизы"),
        db: Session = Depends(get_db)
) :
    """Получение списка квизов"""
    is_public = True if public_only else None
    return crud_quiz.get_quizzes(db, skip=skip, limit=limit, category=category, is_public=is_public)


@router.get("/categories")
def get_categories(db: Session = Depends(get_db)) :
    """Получение всех категорий квизов"""
    return {"categories" : crud_quiz.get_quiz_categories(db)}


@router.get("/{quiz_id}", response_model=schemas.QuizBase)
def read_quiz(quiz_id: int, db: Session = Depends(get_db)) :
    """Получение квиза по ID"""
    db_quiz = crud_quiz.get_quiz(db, quiz_id)
    if db_quiz is None :
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz


@router.get("/{quiz_id}/full")
def read_quiz_full(quiz_id: int, db: Session = Depends(get_db)) :
    """Получение полного квиза со всеми вопросами и ответами"""
    db_quiz = crud_quiz.get_quiz_with_details(db, quiz_id)
    if db_quiz is None :
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz


@router.put("/{quiz_id}", response_model=schemas.QuizBase)
def update_quiz(
        quiz_id: int,
        quiz_update: schemas.QuizUpdate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
) :
    """Обновление квиза"""
    db_quiz = crud_quiz.update_quiz(db, quiz_id, quiz_update)
    if db_quiz is None :
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz


@router.delete("/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
) :
    """Удаление квиза"""
    if not crud_quiz.delete_quiz(db, quiz_id) :
        raise HTTPException(status_code=404, detail="Quiz not found")


"""@router.get("/{quiz_id}/leaderboard")
def get_leaderboard(
        quiz_id: int,
        limit: int = Query(10, ge=1, le=100),
        db: Session = Depends(get_db)
) :
    "Получение таблицы лидеров для квиза"
    # Проверяем существование квиза
    if not crud_quiz.get_quiz(db, quiz_id) :
        raise HTTPException(status_code=404, detail="Quiz not found")
    return crud_quiz.get_quiz_leaderboard(db, quiz_id, limit)
"""


@router.post("/bulk", response_model=schemas.QuizBulkResponse, status_code=status.HTTP_201_CREATED)
def create_quiz_bulk(
        quiz_data: schemas.QuizBulkCreate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
) :
    """
    Массовое создание квиза с вопросами и ответами за один запрос

    Пример тела запроса:
    {
        "title": "Python Basics Quiz",
        "category": "Programming",
        "description": "Test your Python knowledge",
        "is_public": true,
        "quiz_mode": "single",
        "questions": [
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
    result = crud_quiz.create_quiz_full(db, quiz_data)
    return result


