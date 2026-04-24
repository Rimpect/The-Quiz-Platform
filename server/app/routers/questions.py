from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db
from app.utils.security import get_current_user

router = APIRouter(prefix="/quizzes/{quiz_id}/questions", tags=["questions"])

@router.post("/", response_model=schemas.Question, status_code=status.HTTP_201_CREATED)
def create_question(
    quiz_id: int,
    question: schemas.QuestionCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Создание вопроса в квизе"""
    # Проверяем существование квиза
    if not crud.get_quiz(db, quiz_id):
        raise HTTPException(status_code=404, detail="Quiz not found")
    return crud.create_question(db, question, quiz_id)

@router.get("/", response_model=List[schemas.Question])
def read_questions(
    quiz_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получение всех вопросов квиза"""
    return crud.get_questions_by_quiz(db, quiz_id, skip, limit)

@router.get("/{question_id}", response_model=schemas.Question)
def read_question(
    quiz_id: int,
    question_id: int,
    db: Session = Depends(get_db)
):
    """Получение вопроса по ID"""
    question = crud.get_question(db, question_id)
    if not question or question.quiz_id != quiz_id:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.put("/{question_id}", response_model=schemas.Question)
def update_question(
    quiz_id: int,
    question_id: int,
    question_update: schemas.QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Обновление вопроса"""
    question = crud.get_question(db, question_id)
    if not question or question.quiz_id != quiz_id:
        raise HTTPException(status_code=404, detail="Question not found")
    return crud.update_question(db, question_id, question_update)

@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(
    quiz_id: int,
    question_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Удаление вопроса"""
    question = crud.get_question(db, question_id)
    if not question or question.quiz_id != quiz_id:
        raise HTTPException(status_code=404, detail="Question not found")
    crud.delete_question(db, question_id)