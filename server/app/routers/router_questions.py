from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..crud import crud_question as crud_question, crud_quiz as crud_quiz

from ..database.database import get_db
from ..schemas.schemas_question import QuestionBase, QuestionCreate, QuestionUpdate

# from ..utils.security import get_current_user

router = APIRouter(prefix="/quizzes/{quiz_id}/questions", tags=["questions"])


@router.post("/", response_model=QuestionBase, status_code=status.HTTP_201_CREATED)
def create_question(
        quiz_id: int,
        question: QuestionCreate,
        db: Session = Depends(get_db),
        # current_user: User = Depends(get_current_user)
):
    """Создание вопроса в квизе"""
    # Проверяем существование квиза
    if not crud_quiz.get_quiz(db, quiz_id):
        raise HTTPException(status_code=404, detail="Quiz not found")
    return crud_question.create_question(db, question, quiz_id)


@router.get("/", response_model=List[QuestionBase])
def read_questions(
        quiz_id: int,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    """Получение всех вопросов квиза"""
    return crud_question.get_questions_by_quiz(db, quiz_id, skip, limit)


@router.get("/{question_id}", response_model=QuestionBase)
def read_question(
        quiz_id: int,
        question_id: int,
        db: Session = Depends(get_db)
):
    """Получение вопроса по ID"""
    question = crud_question.get_question(db, question_id)
    if not question or question.quiz_id != quiz_id:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.put("/{question_id}", response_model=QuestionBase)
def update_question(
        quiz_id: int,
        question_id: int,
        question_update: QuestionUpdate,
        db: Session = Depends(get_db),
        # current_user: User = Depends(get_current_user)
):
    """Обновление вопроса"""
    question = crud_question.get_question(db, question_id)
    if not question or question.quiz_id != quiz_id:
        raise HTTPException(status_code=404, detail="Question not found")
    return crud_question.update_question(db, question_id, question_update)


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(
        quiz_id: int,
        question_id: int,
        db: Session = Depends(get_db),
        # current_user: User = Depends(get_current_user)
):
    """Удаление вопроса"""
    question = crud_question.get_question(db, question_id)
    if not question or question.quiz_id != quiz_id:
        raise HTTPException(status_code=404, detail="Question not found")
    crud_question.delete_question(db, question_id)
