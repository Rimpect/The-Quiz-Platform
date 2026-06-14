from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from ..database.database import get_db
from ..schemas.schemas_answer import AnswerBase, AnswerUpdate, AnswerCreate
from ..schemas.schemas_user import UserResponse
from ..services import answer_service
from ..utils.security import get_current_user

router = APIRouter(prefix="/questions/{question_id}/answers", tags=["answers"])


@router.post("", response_model=AnswerBase, status_code=status.HTTP_201_CREATED)
def create_answer(
        question_id: int,
        answer: AnswerCreate,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    return answer_service.create_answer(db, question_id, answer)


@router.post("/bulk", response_model=List[AnswerBase], status_code=status.HTTP_201_CREATED)
def create_answers_bulk(
        question_id: int,
        answers: List[AnswerCreate],
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Массовое создание вариантов ответов"""
    return answer_service.create_answers_bulk(db, question_id, answers)


@router.get("", response_model=List[AnswerBase])
def read_answers(question_id: int, db: Session = Depends(get_db)):
    """Получение всех вариантов ответов для вопроса"""
    return answer_service.get_answers(db, question_id)


@router.get("/{answer_id}", response_model=AnswerBase)
def read_answer(question_id: int, answer_id: int, db: Session = Depends(get_db)):
    """Получение варианта ответа по ID"""
    return answer_service.get_answer(db, question_id, answer_id)


@router.put("/{answer_id}", response_model=AnswerBase)
def update_answer(
        question_id: int,
        answer_id: int,
        answer_update: AnswerUpdate,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Обновление варианта ответа"""
    return answer_service.update_answer(db, question_id, answer_id, answer_update)


@router.delete("/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(
        question_id: int,
        answer_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Удаление варианта ответа"""
    answer_service.delete_answer(db, question_id, answer_id)
