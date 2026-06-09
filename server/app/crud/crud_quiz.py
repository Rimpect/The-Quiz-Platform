from datetime import datetime
from typing import Optional, List, Dict, Any
from typing import Type

from sqlalchemy.orm import Session, joinedload

from .. import schemas
from ..models.model_answer import Answer
from ..models.model_pending_quiz import PendingQuiz, PendingQuizStatus
from ..models.model_question import Question as Quest
from ..models.model_quiz import Quiz


def get_quiz(db: Session, quiz_id: int) -> Optional[Quiz]:
    return db.query(Quiz).filter(Quiz.id == quiz_id).first()


def get_quiz_questions(db: Session, quiz_id):
    return db.query(Quest).filter(quiz_id == Quest.quiz_id)


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

def get_available_quizzes_for_user(
        db: Session,
        user=None,
        is_guest: bool = False,
        skip: int = 0,
        limit: int = 100
):
    query = db.query(Quiz)

    if is_guest:
        query = query.filter(
            Quiz.is_public == True,
            Quiz.quiz_mode == "single"
        )
    else:
        query.filter(Quiz.is_public == True)

    return query.offset(skip).limit(limit).all()


def can_guest_access_quiz(
        db: Session,
        quiz_id: int
) -> bool:
    quiz = get_quiz(db, quiz_id)
    if not quiz:
        return


# ========== ОПЕРАЦИИ С ОДОБРЕННЫМИ КВИЗАМИ ==========

def get_quiz(db: Session, quiz_id: int) -> Optional[Quiz] :
    return db.query(Quiz).options(joinedload(Quiz.category_ref)).filter(Quiz.id == quiz_id).first()


def get_quizzes(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None,
        author_id: Optional[int] = None,
        is_public: Optional[bool] = True
) -> List[Quiz] :
    query = db.query(Quiz).options(joinedload(Quiz.category_ref))

    if category_id :
        query = query.filter(Quiz.category_id == category_id)
    if author_id :
        query = query.filter(Quiz.author_id == author_id)
    if is_public is not None :
        query = query.filter(Quiz.is_public == is_public)

    return query.order_by(Quiz.created_at.desc()).offset(skip).limit(limit).all()


def create_quiz(db: Session, quiz: schemas.QuizCreate, author_id: int) -> Quiz :
    """Создание квиза (сразу в опубликованные, без модерации)"""
    db_quiz = Quiz(
        title=quiz.title,
        category_id=quiz.category_id,
        description=quiz.description,
        cover_url=quiz.cover_url,
        is_public=quiz.is_public,
        quiz_mode=quiz.quiz_mode,
        author_id=author_id
    )
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz


def create_quiz_pending(db: Session, quiz: schemas.QuizCreate, author_id: int) -> PendingQuiz :
    """Создание квиза на модерацию"""
    db_pending = PendingQuiz(
        title=quiz.title,
        category_id=quiz.category_id,
        description=quiz.description,
        cover_url=quiz.cover_url,
        quiz_mode=quiz.quiz_mode,
        author_id=author_id,
        status=PendingQuizStatus.PENDING
    )
    db.add(db_pending)
    db.commit()
    db.refresh(db_pending)
    return db_pending


def update_quiz(db: Session, quiz_id: int, quiz_update: schemas.QuizUpdate, user_id: int) -> Optional[Quiz] :
    """Обновление квиза (только автор)"""
    db_quiz = get_quiz(db, quiz_id)
    if db_quiz and db_quiz.author_id == user_id :
        update_data = quiz_update.model_dump(exclude_unset=True)
        for field, value in update_data.items() :
            setattr(db_quiz, field, value)
        db_quiz.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_quiz)
    return db_quiz


def delete_quiz(db: Session, quiz_id: int, user_id: int, is_admin: bool = False) -> bool :
    """Удаление квиза (автор или админ)"""
    db_quiz = get_quiz(db, quiz_id)
    if db_quiz and (db_quiz.author_id == user_id or is_admin) :
        db.delete(db_quiz)
        db.commit()
        return True
    return False


# ========== ОПЕРАЦИИ С КВИЗАМИ НА МОДЕРАЦИИ ==========

def get_pending_quiz(db: Session, pending_id: int) -> Optional[PendingQuiz] :
    return db.query(PendingQuiz).filter(PendingQuiz.id == pending_id).first()


def get_pending_quizzes(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[PendingQuizStatus] = None,
        author_id: Optional[int] = None
) -> List[PendingQuiz] :
    query = db.query(PendingQuiz)

    if status :
        query = query.filter(PendingQuiz.status == status)
    if author_id :
        query = query.filter(PendingQuiz.author_id == author_id)

    return query.order_by(PendingQuiz.created_at.desc()).offset(skip).limit(limit).all()


def update_pending_quiz_status(
        db: Session,
        pending_id: int,
        status: PendingQuizStatus,
        moderator_id: int
) -> Optional[PendingQuiz] :
    """Обновление статуса квиза на модерации"""
    pending = get_pending_quiz(db, pending_id)
    if pending :
        pending.status = status
        pending.moderated_at = datetime.utcnow()
        pending.moderated_by = moderator_id
        db.commit()
        db.refresh(pending)
    return pending


def approve_pending_quiz(db: Session, pending_id: int, moderator_id: int) -> Optional[Quiz] :
    """Одобрение квиза: перенос из pending в опубликованные"""
    pending = get_pending_quiz(db, pending_id)
    if not pending or pending.status != PendingQuizStatus.PENDING :
        return None

    # Создаём опубликованный квиз
    new_quiz = Quiz(
        title=pending.title,
        category_id=pending.category_id,
        description=pending.description,
        cover_url=pending.cover_url,
        quiz_mode=pending.quiz_mode,
        is_public=True,
        author_id=pending.author_id
    )
    db.add(new_quiz)
    db.flush()  # Получаем ID нового квиза

    # Копируем вопросы и ответы (если они есть в pending)
    # Здесь нужно скопировать связанные данные

    # Обновляем статус pending
    pending.status = PendingQuizStatus.APPROVED
    pending.moderated_at = datetime.utcnow()
    pending.moderated_by = moderator_id

    db.commit()
    db.refresh(new_quiz)
    return new_quiz


def reject_pending_quiz(db: Session, pending_id: int, moderator_id: int) -> bool :
    """Отклонение квиза: удаление из pending"""
    pending = get_pending_quiz(db, pending_id)
    if pending and pending.status == PendingQuizStatus.PENDING :
        pending.status = PendingQuizStatus.REJECTED
        pending.moderated_at = datetime.utcnow()
        pending.moderated_by = moderator_id
        db.commit()
        db.delete(pending)
        db.commit()
        return True
    return False


def delete_pending_quiz(db: Session, pending_id: int, user_id: int, is_admin: bool = False) -> bool :
    """Удаление квиза из модерации (автор или админ)"""
    pending = get_pending_quiz(db, pending_id)
    if pending and (pending.author_id == user_id or is_admin) :
        db.delete(pending)
        db.commit()
        return True
    return False


# ========== ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ ==========

def get_user_quizzes(db: Session, user_id: int) -> Dict[str, Any] :
    """Получение всех квизов пользователя (опубликованных и на модерации)"""
    published = get_quizzes(db, author_id=user_id, is_public=True)
    pending = get_pending_quizzes(db, author_id=user_id, status=PendingQuizStatus.PENDING)

    return {
        "published" : published,
        "pending" : pending
    }
