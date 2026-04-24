from sqlalchemy.orm import Session
from app import models, schemas
from typing import Optional, List

def get_answer(db: Session, answer_id: int) -> Optional[models.Answer]:
    return db.query(models.Answer).filter(models.Answer.id == answer_id).first()

def get_answers_by_question(db: Session, question_id: int) -> List[models.Answer]:
    return db.query(models.Answer).filter(
        models.Answer.question_id == question_id
    ).order_by(models.Answer.order_number).all()

def create_answer(db: Session, answer: schemas.AnswerCreate, question_id: int) -> models.Answer:
    db_answer = models.Answer(
        **answer.model_dump(),
        question_id=question_id
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

def create_answers_bulk(db: Session, answers: List[schemas.AnswerCreate], question_id: int) -> List[models.Answer]:
    db_answers = []
    for answer in answers:
        db_answer = models.Answer(
            **answer.model_dump(),
            question_id=question_id
        )
        db.add(db_answer)
        db_answers.append(db_answer)
    db.commit()
    for answer in db_answers:
        db.refresh(answer)
    return db_answers

def update_answer(db: Session, answer_id: int, answer_update: schemas.AnswerUpdate) -> Optional[models.Answer]:
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
    result = db.query(models.Answer).filter(
        models.Answer.question_id == question_id
    ).delete()
    db.commit()
    return result