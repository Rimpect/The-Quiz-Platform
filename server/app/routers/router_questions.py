from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database.database import get_db
from ..models.model_user import User
from ..schemas.schemas_question import QuestionBase, QuestionCreate, QuestionUpdate, QuestionResponse
from ..utils.security import get_current_user, get_current_user_or_guest_optional
from ..services import QuestionService

router = APIRouter(prefix="/quizzes/{quiz_id}/questions", tags=["questions"])


def get_question_service(db: Session = Depends(get_db)) -> QuestionService:
    """Dependency для получения экземпляра QuestionService"""
    return QuestionService(db)


@router.post("", response_model=QuestionBase, status_code=status.HTTP_201_CREATED)
def create_question(
        quiz_id: int,
        question: QuestionCreate,
        question_service: QuestionService = Depends(get_question_service),
        current_user: User = Depends(get_current_user)
):
    """Создание вопроса в квизе"""
    try:
        return question_service.create_question(question, quiz_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=List[QuestionResponse])
def read_questions(
        quiz_id: int,
        skip: int = 0,
        limit: int = 100,
        question_service: QuestionService = Depends(get_question_service),
        current_user=Depends(get_current_user_or_guest_optional)
):
    """Получение всех вопросов квиза с вариантами ответов (доступно гостям)"""
    questions = question_service.get_questions_by_quiz(quiz_id, skip, limit)
    return questions


@router.get("/{question_id}", response_model=QuestionBase)
def read_question(
        quiz_id: int,
        question_id: int,
        question_service: QuestionService = Depends(get_question_service),
        current_user: User = Depends(get_current_user)
):
    """Получение вопроса по ID"""
    question = question_service.get_question(question_id)
    if not question or not question_service.check_question_belongs_to_quiz(question_id, quiz_id):
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.put("/{question_id}", response_model=QuestionBase)
def update_question(
        quiz_id: int,
        question_id: int,
        question_update: QuestionUpdate,
        question_service: QuestionService = Depends(get_question_service),
        current_user: User = Depends(get_current_user)
):
    """Обновление вопроса"""
    if not question_service.check_question_belongs_to_quiz(question_id, quiz_id):
        raise HTTPException(status_code=404, detail="Question not found")
    
    updated = question_service.update_question(question_id, question_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Question not found")
    return updated


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(
        quiz_id: int,
        question_id: int,
        question_service: QuestionService = Depends(get_question_service),
        current_user: User = Depends(get_current_user)
):
    """Удаление вопроса"""
    if not question_service.check_question_belongs_to_quiz(question_id, quiz_id):
        raise HTTPException(status_code=404, detail="Question not found")
    
    question_service.delete_question(question_id)
