from sqlalchemy.orm import Session
from ..models.model_answer import Answer
from ..schemas.schemas_answer import *
from typing import Optional, List, Type


def get_answer(db: Session, answer_id: int) -> Optional[Answer]:
    return db.query(Answer).filter(Answer.id == answer_id).first()


def get_answers_by_question(db: Session, question_id: int) -> List[Answer]:
    return db.query(Answer).filter(
        Answer.question_id == question_id
    ).order_by(Answer.order_number).all()


def create_answer(db: Session, answer: AnswerCreate, question_id: int) -> Answer:
    db_answer = Answer(
        **answer.model_dump(),
        question_id=question_id
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def create_answers_bulk(db: Session, answers: List[AnswerCreate], question_id: int) -> List[Answer]:
    db_answers = []
    for answer in answers:
        db_answer = Answer(
            **answer.model_dump(),
            question_id=question_id
        )
        db.add(db_answer)
        db_answers.append(db_answer)
    db.commit()
    for answer in db_answers:
        db.refresh(answer)
    return db_answers


def update_answer(db: Session, answer_id: int, answer_update: AnswerUpdate) -> Optional[Answer]:
    db_answer = get_answer(db, answer_id)
    if db_answer:
        update_data = answer_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_answer, field, value)
        db.commit()
        db.refresh(db_answer)
    return db_answer


def delete_answer(db: Session, answer_id: int) -> bool:
    db_answer = get_answer(db, answer_id)
    if db_answer:
        db.delete(db_answer)
        db.commit()
        return True
    return False


def delete_answers_by_question(db: Session, question_id: int) -> int:
    result = db.query(Answer).filter(
        Answer.question_id == question_id
    ).delete()
    db.commit()
    return result


def get_correct_answers(db, question_id) -> List[Answer]:
    return db.query(Answer).filter(Answer.question_id == question_id,
                                   Answer.is_correct == True).all()