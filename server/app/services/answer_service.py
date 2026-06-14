"""Бизнес-логика вариантов ответов (HTTP-агностична)."""
from typing import List

from sqlalchemy.orm import Session

from ..crud import crud_answer, crud_question
from ..schemas.schemas_answer import AnswerCreate, AnswerUpdate
from .exceptions import NotFoundError


def create_answer(db: Session, question_id: int, answer: AnswerCreate):
    if not crud_question.get_question(db, question_id):
        raise NotFoundError("Question not found")
    return crud_answer.create_answer(db, answer, question_id)


def create_answers_bulk(db: Session, question_id: int, answers: List[AnswerCreate]):
    if not crud_question.get_question(db, question_id):
        raise NotFoundError("Question not found")
    return crud_answer.create_answers_bulk(db, answers, question_id)


def get_answers(db: Session, question_id: int):
    return crud_answer.get_answers_by_question(db, question_id)


def get_answer(db: Session, question_id: int, answer_id: int):
    answer = crud_answer.get_answer(db, answer_id)
    if not answer or answer.question_id != question_id:
        raise NotFoundError("Answer not found")
    return answer


def update_answer(db: Session, question_id: int, answer_id: int, answer_update: AnswerUpdate):
    get_answer(db, question_id, answer_id)
    return crud_answer.update_answer(db, answer_id, answer_update)


def delete_answer(db: Session, question_id: int, answer_id: int):
    get_answer(db, question_id, answer_id)
    crud_answer.delete_answer(db, answer_id)
