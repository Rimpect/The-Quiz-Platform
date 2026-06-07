from datetime import datetime
from typing import Optional, List, Type, Any, Dict

from sqlalchemy.orm import Session, joinedload

from .. import schemas
from ..models.model_question import Question as Quest
from ..models.model_quiz import Quiz
from ..models.model_answer import Answer


def get_quiz(db: Session, quiz_id: int) -> Optional[Quiz]:
    return db.query(Quiz).filter(Quiz.id == quiz_id).first()


def get_quiz_questions(db: Session, quiz_id):
    return db.query(Quest).filter(quiz_id == Quest.quiz_id)


def get_quizzes(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        is_public: Optional[bool] = None
) -> list[Type[Quiz]]:
    query = db.query(Quiz)
    if category:
        query = query.filter(Quiz.category == category)
    if is_public is not None:
        query = query.filter(Quiz.is_public == is_public)
    return query.offset(skip).limit(limit).all()


def create_quiz(db: Session, quiz: schemas.QuizCreate) -> Quiz:
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


def update_quiz(db: Session, quiz_id: int, quiz_update: schemas.QuizUpdate) -> Optional[Quiz]:
    db_quiz = get_quiz(db, quiz_id)
    if db_quiz:
        update_data = quiz_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_quiz, field, value)
        db_quiz.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_quiz)
    return db_quiz


def update_quiz_cover(db: Session, quiz_id: int, cover_url: str) -> Optional[Quiz]:
    db_quiz = get_quiz(db, quiz_id)
    if db_quiz:
        db_quiz.cover_url = cover_url
        db_quiz.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_quiz)
    return db_quiz


def delete_quiz(db: Session, quiz_id: int) -> bool:
    db_quiz = get_quiz(db, quiz_id)
    if db_quiz:
        db.delete(db_quiz)
        db.commit()
        return True
    return False


def get_quiz_with_details(db: Session, quiz_id: int) -> Optional[Quiz]:
    """Получение квиза со всеми вопросами и ответами"""
    return db.query(Quiz).options(
        joinedload(Quiz.questions).joinedload(Quest.answers)
    ).filter(Quiz.id == quiz_id).first()


def get_quiz_categories(db: Session) -> List[str]:
    """Получение всех уникальных категорий"""
    categories = db.query(Quiz.category).distinct().all()
    return [cat[0] for cat in categories]


def create_quiz_full(
        db: Session,
        quiz_data: schemas.QuizBulkCreate
) -> Dict[str, Any]:
    """
    Массовое создание квиза с вопросами и ответами

    Args:
        db: Сессия БД
        quiz_data: Данные квиза с вопросами и ответами

    Returns:
        Словарь с созданным квизом, количеством вопросов и ответов
    """

    # 1. Создаем квиз
    db_quiz: Quiz = Quiz(
        title=quiz_data.title,
        category=quiz_data.category,
        description=quiz_data.description,
        cover_url=quiz_data.cover_url,
        is_public=quiz_data.is_public,
        quiz_mode=quiz_data.quiz_mode
    )
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)

    questions_created = 0
    answers_created = 0

    # 2. Создаем вопросы и ответы
    for idx, q_data in enumerate(quiz_data.questions):
        # Создаем вопрос
        db_question = Quest(
            quiz_id=db_quiz.id,
            answer_type=q_data.answer_type,
            points=q_data.points,
            question_text=q_data.question_text,
            media_url=q_data.media_url,
            time_limit_seconds=q_data.time_limit_seconds,
            order_number=idx
        )
        db.add(db_question)
        db.flush()
        questions_created += 1

        # Создаем ответы для вопроса
        for ans_idx, a_data in enumerate(q_data.answers):
            db_answer = Answer(
                question_id=db_question.id,
                answer_text=a_data.answer_text,
                is_correct=a_data.is_correct,
                order_number=a_data.order_number or ans_idx
            )
            db.add(db_answer)
            answers_created += 1

    db.commit()

    # Загружаем полный квиз со всеми связями
    result = db.query(Quiz).options(
        joinedload(Quiz.questions).joinedload(Quest.answers)
    ).filter(db_quiz.id == Quiz.id).first()

    # Обновляем количество вопросов в квизе
    db_quiz.total_questions = questions_created
    db.commit()

    return {
        "quiz": result,
        "questions_created": questions_created,
        "answers_created": answers_created,
        "total_time_limit_minutes": db_quiz.duration_minutes
    }
