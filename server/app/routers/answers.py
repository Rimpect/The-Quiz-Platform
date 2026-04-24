from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db
from app.utils.security import get_current_user

router = APIRouter(prefix="/questions/{question_id}/answers", tags=["answers"])

@router.post("/", response_model=schemas.Answer, status_code=status.HTTP_201_CREATED)
def create_answer(
    question_id: int,
    answer: schemas.AnswerCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Создание варианта ответа для вопроса"""
    if not crud.get_question(db, question_id):
        raise HTTPException(status_code=404, detail="Question not found")
    return crud.create_answer(db, answer, question_id)

@router.post("/bulk", response_model=List[schemas.Answer], status_code=status.HTTP_201_CREATED)
def create_answers_bulk(
    question_id: int,
    answers: List[schemas.AnswerCreate],
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Массовое создание вариантов ответов"""
    if not crud.get_question(db, question_id):
        raise HTTPException(status_code=404, detail="Question not found")
    return crud.create_answers_bulk(db, answers, question_id)

@router.get("/", response_model=List[schemas.Answer])
def read_answers(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Получение всех вариантов ответов для вопроса"""
    return crud.get_answers_by_question(db, question_id)

@router.get("/{answer_id}", response_model=schemas.Answer)
def read_answer(
    question_id: int,
    answer_id: int,
    db: Session = Depends(get_db)
):
    """Получение варианта ответа по ID"""
    answer = crud.get_answer(db, answer_id)
    if not answer or answer.question_id != question_id:
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer

@router.put("/{answer_id}", response_model=schemas.Answer)
def update_answer(
    question_id: int,
    answer_id: int,
    answer_update: schemas.AnswerUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Обновление варианта ответа"""
    answer = crud.get_answer(db, answer_id)
    if not answer or answer.question_id != question_id:
        raise HTTPException(status_code=404, detail="Answer not found")
    return crud.update_answer(db, answer_id, answer_update)

@router.delete("/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(
    question_id: int,
    answer_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Удаление варианта ответа"""
    answer = crud.get_answer(db, answer_id)
    if not answer or answer.question_id != question_id:
        raise HTTPException(status_code=404, detail="Answer not found")
    crud.delete_answer(db, answer_id)