from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from ..database.database import get_db
from ..models.model_user import User
from ..schemas.schemas_question import QuestionBase, QuestionCreate, QuestionUpdate, QuestionResponse
from ..services import question_service
from ..utils.security import get_current_user, get_current_user_or_guest_optional

router = APIRouter(prefix="/quizzes/{quiz_id}/questions", tags=["questions"])


@router.post("", response_model=QuestionBase, status_code=status.HTTP_201_CREATED)
def create_question(
        quiz_id: int,
        question: QuestionCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Создание вопроса в квизе"""
    return question_service.create_question(db, quiz_id, question)


@router.get("", response_model=List[QuestionResponse])
def read_questions(
        quiz_id: int,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user_or_guest_optional)
):
    """Получение всех вопросов квиза с вариантами ответов (доступно гостям)"""
    return question_service.get_questions(db, quiz_id, skip, limit)


@router.get("/{question_id}", response_model=QuestionBase)
def read_question(
        quiz_id: int,
        question_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получение вопроса по ID"""
    return question_service.get_question(db, quiz_id, question_id)


@router.put("/{question_id}", response_model=QuestionBase)
def update_question(
        quiz_id: int,
        question_id: int,
        question_update: QuestionUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Обновление вопроса"""
    return question_service.update_question(db, quiz_id, question_id, question_update)


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(
        quiz_id: int,
        question_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Удаление вопроса"""
    question_service.delete_question(db, quiz_id, question_id)
