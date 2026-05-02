from sqlalchemy.orm import Session
from ..models.model_question import Question as Quest
from ...app import schemas
from datetime import datetime
from typing import Optional, List, Type


def get_question(db: Session, question_id: int) -> Optional[Quest] :
    return db.query(Quest).filter(Quest.id == question_id).first()


def get_questions_by_quiz(db: Session, quiz_id: int, skip: int = 0, limit: int = 100) -> list[Type[Quest]] :
    return db.query(Quest).filter(
        Quest.quiz_id == quiz_id
    ).offset(skip).limit(limit).all()


def create_question(db: Session, question: schemas.QuestionCreate, quiz_id: int) -> Quest:
    db_question = Quest(
        **question.model_dump(),
        quiz_id=quiz_id
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def update_question(db: Session, question_id: int, question_update: schemas.QuestionUpdate) -> Optional[
    Quest] :
    db_question = get_question(db, question_id)
    if db_question :
        update_data = question_update.model_dump(exclude_unset=True)
        for field, value in update_data.items() :
            setattr(db_question, field, value)
        db_question.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_question)
    return db_question


def delete_question(db: Session, question_id: int) -> bool :
    db_question = get_question(db, question_id)
    if db_question :
        db.delete(db_question)
        db.commit()
        return True
    return False


def update_question_media(db: Session, question_id: int, media_url: str) -> Optional[Quest] :
    db_question = get_question(db, question_id)
    if db_question :
        db_question.media_url = media_url
        db_question.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_question)
    return db_question
