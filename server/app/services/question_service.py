from sqlalchemy.orm import Session

from ..crud import crud_question, crud_quiz
from ..schemas.schemas_question import QuestionCreate, QuestionUpdate
from .exceptions import NotFoundError

def create_question(db: Session, quiz_id: int, question: QuestionCreate):
    if not crud_quiz.get_quiz(db, quiz_id):
        raise NotFoundError("Quiz not found")
    return crud_question.create_question(db, question, quiz_id)

def get_questions(db: Session, quiz_id: int, skip: int = 0, limit: int = 100):
    return crud_question.get_questions_by_quiz(db, quiz_id, skip, limit)

def get_question(db: Session, quiz_id: int, question_id: int):
    question = crud_question.get_question(db, question_id)
    if not question or question.quiz_id != quiz_id:
        raise NotFoundError("Question not found")
    return question

def update_question(db: Session, quiz_id: int, question_id: int, question_update: QuestionUpdate):
    get_question(db, quiz_id, question_id)
    return crud_question.update_question(db, question_id, question_update)

def delete_question(db: Session, quiz_id: int, question_id: int):
    get_question(db, quiz_id, question_id)
    crud_question.delete_question(db, question_id)
