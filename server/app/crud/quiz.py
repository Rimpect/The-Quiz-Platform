from sqlalchemy.orm import Session, joinedload
from ..models.model_quiz import Quiz
from ..models.model_question import Question as Quest
from ...app import schemas
from datetime import datetime
from typing import Optional, List, Type


def get_quiz(db: Session, quiz_id: int) -> Optional[Quiz]:
    return db.query(Quiz).filter(Quiz.id == quiz_id).first()


def get_quizzes(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        is_public: Optional[bool] = None
) -> list[Type[Quiz]]:
    query = db.query(Quiz)
    if category :
        query = query.filter(Quiz.category == category)
    if is_public is not None :
        query = query.filter(Quiz.is_public == is_public)
    return query.offset(skip).limit(limit).all()


def create_quiz(db: Session, quiz: schemas.QuizCreate) -> Quiz :
    db_quiz = Quiz(
        title=quiz.title,
        category=quiz.category,
        description=quiz.description,
        cover_url=quiz.cover_url,
        is_public=quiz.is_public,
        quiz_mode=quiz.quiz_mode
    )
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz


def update_quiz(db: Session, quiz_id: int, quiz_update: schemas.QuizUpdate) -> Optional[Quiz] :
    db_quiz = get_quiz(db, quiz_id)
    if db_quiz :
        update_data = quiz_update.model_dump(exclude_unset=True)
        for field, value in update_data.items() :
            setattr(db_quiz, field, value)
        db_quiz.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_quiz)
    return db_quiz


def update_quiz_cover(db: Session, quiz_id: int, cover_url: str) -> Optional[Quiz] :
    db_quiz = get_quiz(db, quiz_id)
    if db_quiz :
        db_quiz.cover_url = cover_url
        db_quiz.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_quiz)
    return db_quiz


def delete_quiz(db: Session, quiz_id: int) -> bool :
    db_quiz = get_quiz(db, quiz_id)
    if db_quiz :
        db.delete(db_quiz)
        db.commit()
        return True
    return False


def get_quiz_with_details(db: Session, quiz_id: int) -> Optional[Quiz] :
    """Получение квиза со всеми вопросами и ответами"""
    return db.query(Quiz).options(
        joinedload(Quiz.questions).joinedload(Quest.answers)
    ).filter(Quiz.id == quiz_id).first()


def get_quiz_categories(db: Session) -> List[str] :
    """Получение всех уникальных категорий"""
    categories = db.query(Quiz.category).distinct().all()
    return [cat[0] for cat in categories]
