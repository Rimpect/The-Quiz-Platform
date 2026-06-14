from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database.database import get_db
from ..schemas.schemas_answer import AnswerBase, AnswerUpdate, AnswerCreate
from ..schemas.schemas_user import UserResponse
from ..utils.security import get_current_user
from ..services.service_answer import AnswerService

router = APIRouter(prefix="/questions/{question_id}/answers", tags=["answers"])


def get_answer_service(db: Session = Depends(get_db)) -> AnswerService:
    """Dependency для получения экземпляра AnswerService"""
    return AnswerService(db)


@router.post("", response_model=AnswerBase, status_code=status.HTTP_201_CREATED)
def create_answer(
        question_id: int,
        answer: AnswerCreate,
        answer_service: AnswerService = Depends(get_answer_service),
        current_user: UserResponse = Depends(get_current_user)
):
    """Создание ответа на вопрос"""
    try:
        return answer_service.create_answer(answer, question_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/bulk", response_model=List[AnswerBase], status_code=status.HTTP_201_CREATED)
def create_answers_bulk(
        question_id: int,
        answers: List[AnswerCreate],
        answer_service: AnswerService = Depends(get_answer_service),
        current_user: UserResponse = Depends(get_current_user)
):
    """Массовое создание вариантов ответов"""
    try:
        return answer_service.create_answers_bulk(answers, question_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=List[AnswerBase])
def read_answers(
        question_id: int,
        answer_service: AnswerService = Depends(get_answer_service)
):
    """Получение всех вариантов ответов для вопроса"""
    return answer_service.get_answers_by_question(question_id)


@router.get("/{answer_id}", response_model=AnswerBase)
def read_answer(
        question_id: int,
        answer_id: int,
        answer_service: AnswerService = Depends(get_answer_service)
):
    """Получение варианта ответа по ID"""
    answer = answer_service.get_answer(answer_id)
    if not answer or not answer_service.check_answer_belongs_to_question(answer_id, question_id):
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer


@router.put("/{answer_id}", response_model=AnswerBase)
def update_answer(
        question_id: int,
        answer_id: int,
        answer_update: AnswerUpdate,
        answer_service: AnswerService = Depends(get_answer_service),
        current_user: UserResponse = Depends(get_current_user)
):
    """Обновление варианта ответа"""
    if not answer_service.check_answer_belongs_to_question(answer_id, question_id):
        raise HTTPException(status_code=404, detail="Answer not found")
    
    updated = answer_service.update_answer(answer_id, answer_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Answer not found")
    return updated


@router.delete("/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(
        question_id: int,
        answer_id: int,
        answer_service: AnswerService = Depends(get_answer_service),
        current_user: UserResponse = Depends(get_current_user)
):
    """Удаление варианта ответа"""
    if not answer_service.check_answer_belongs_to_question(answer_id, question_id):
        raise HTTPException(status_code=404, detail="Answer not found")
    
    answer_service.delete_answer(answer_id)
