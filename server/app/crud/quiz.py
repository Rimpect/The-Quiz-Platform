from datetime import datetime
from typing import Optional, List, Type, Any, Dict

from sqlalchemy.orm import Session, joinedload

from .. import schemas
from ..models.model_question import Question as Quest
from ..models.model_quiz import Quiz


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


def create_quiz_bulk(
        db: Session,
        quiz_data: schemas.QuizBulkCreate
) -> Dict[str, Any] :
    """
    Массовое создание квиза с вопросами и ответами

    Args:
        db: Сессия БД
        quiz_data: Данные квиза с вопросами и ответами

    Returns:
        Словарь с созданным квизом, количеством вопросов и ответов
    """

    # 1. Создаем квиз
    db_quiz = Quiz(
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
    for idx, q_data in enumerate(quiz_data.questions) :
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
        for ans_idx, a_data in enumerate(q_data.answers) :
            db_answer = models.Answer(
                question_id=db_question.id,
                answer_text=a_data.answer_text,
                is_correct=a_data.is_correct,
                order_number=a_data.order_number or ans_idx
            )
            db.add(db_answer)
            answers_created += 1

    db.commit()

    # Загружаем полный квиз со всеми связями
    result = db.query(models.Quiz).options(
        joinedload(models.Quiz.questions).joinedload(models.Question.answers)
    ).filter(models.Quiz.id == db_quiz.id).first()

    # Обновляем количество вопросов в квизе
    db_quiz.total_questions = questions_created
    db.commit()

    return {
        "quiz" : result,
        "questions_created" : questions_created,
        "answers_created" : answers_created,
        "total_time_limit_minutes" : db_quiz.duration_minutes
    }


def update_quiz_bulk(
        db: Session,
        quiz_id: int,
        quiz_data: schemas.QuizUpdateBulk
) -> Optional[Dict[str, Any]] :
    """
    Массовое обновление квиза (добавление/обновление/удаление вопросов и ответов)

    Args:
        db: Сессия БД
        quiz_id: ID квиза
        quiz_data: Данные для обновления

    Returns:
        Словарь с результатами обновления
    """
    from ..crud import question as crud_question
    from ..crud import answer as crud_answer

    # 1. Проверяем существование квиза
    db_quiz = get_quiz(db, quiz_id)
    if not db_quiz :
        return None

    questions_added = 0
    questions_updated = 0
    questions_deleted = 0
    answers_added = 0
    answers_updated = 0

    # 2. Обновляем поля квиза
    update_data = quiz_data.model_dump(exclude_unset=True, exclude={
        'questions_to_add', 'questions_to_update', 'question_ids_to_delete'
    })
    for field, value in update_data.items() :
        if value is not None :
            setattr(db_quiz, field, value)

    # 3. Добавляем новые вопросы
    for q_data in quiz_data.questions_to_add :
        db_question = models.Question(
            quiz_id=quiz_id,
            answer_type=q_data.answer_type,
            points=q_data.points,
            question_text=q_data.question_text,
            media_url=q_data.media_url,
            time_limit_seconds=q_data.time_limit_seconds
        )
        db.add(db_question)
        db.flush()
        questions_added += 1

        # Добавляем ответы к новому вопросу
        for ans_idx, a_data in enumerate(q_data.answers) :
            db_answer = models.Answer(
                question_id=db_question.id,
                answer_text=a_data.answer_text,
                is_correct=a_data.is_correct,
                order_number=a_data.order_number or ans_idx
            )
            db.add(db_answer)
            answers_added += 1

    # 4. Обновляем существующие вопросы
    for q_data in quiz_data.questions_to_update :
        if q_data.question_id :
            db_question = crud_question.get_question(db, q_data.question_id)
            if db_question and db_question.quiz_id == quiz_id :
                # Обновляем поля вопроса
                if q_data.answer_type is not None :
                    db_question.answer_type = q_data.answer_type
                if q_data.points is not None :
                    db_question.points = q_data.points
                if q_data.question_text is not None :
                    db_question.question_text = q_data.question_text
                if q_data.media_url is not None :
                    db_question.media_url = q_data.media_url
                if q_data.time_limit_seconds is not None :
                    db_question.time_limit_seconds = q_data.time_limit_seconds
                db_question.updated_at = datetime.utcnow()
                questions_updated += 1

                # Обновляем ответы
                if q_data.delete_answers :
                    # Удаляем старые ответы
                    deleted = crud_answer.delete_answers_by_question(db, db_question.id)
                    answers_updated += deleted

                if q_data.answers :
                    for ans_idx, a_data in enumerate(q_data.answers) :
                        # Проверяем, существует ли ответ с таким order_number
                        existing_answer = db.query(models.Answer).filter(
                            models.Answer.question_id == db_question.id,
                            models.Answer.order_number == (a_data.order_number or ans_idx)
                        ).first()

                        if existing_answer :
                            # Обновляем существующий ответ
                            existing_answer.answer_text = a_data.answer_text
                            existing_answer.is_correct = a_data.is_correct
                            answers_updated += 1
                        else :
                            # Создаем новый ответ
                            db_answer = models.Answer(
                                question_id=db_question.id,
                                answer_text=a_data.answer_text,
                                is_correct=a_data.is_correct,
                                order_number=a_data.order_number or ans_idx
                            )
                            db.add(db_answer)
                            answers_added += 1

    # 5. Удаляем вопросы
    for q_id in quiz_data.question_ids_to_delete :
        db_question = crud_question.get_question(db, q_id)
        if db_question and db_question.quiz_id == quiz_id :
            # Сначала удаляем ответы
            crud_answer.delete_answers_by_question(db, q_id)
            # Затем удаляем вопрос
            db.delete(db_question)
            questions_deleted += 1

    db.commit()

    # Обновляем количество вопросов
    db_quiz.total_questions = db.query(models.Question).filter(
        models.Question.quiz_id == quiz_id
    ).count()
    db.commit()

    # Загружаем обновленный квиз
    result = db.query(models.Quiz).options(
        joinedload(models.Quiz.questions).joinedload(models.Question.answers)
    ).filter(models.Quiz.id == quiz_id).first()

    return {
        "quiz" : result,
        "questions_added" : questions_added,
        "questions_updated" : questions_updated,
        "questions_deleted" : questions_deleted,
        "answers_added" : answers_added,
        "answers_updated" : answers_updated
    }


def copy_quiz(
        db: Session,
        source_quiz_id: int,
        new_title: str,
        copy_questions: bool = True
) -> Optional[models.Quiz] :
    """
    Копирование квиза (с вопросами и ответами или без)

    Args:
        db: Сессия БД
        source_quiz_id: ID исходного квиза
        new_title: Новое название для копии
        copy_questions: Копировать ли вопросы и ответы

    Returns:
        Новый квиз
    """
    from ..crud import question as crud_question

    # Получаем исходный квиз
    source_quiz = get_quiz(db, source_quiz_id)
    if not source_quiz :
        return None

    # Создаем копию квиза
    new_quiz = models.Quiz(
        title=new_title,
        category=source_quiz.category,
        description=source_quiz.description,
        cover_url=source_quiz.cover_url,
        is_public=False,  # Копия по умолчанию не публичная
        quiz_mode=source_quiz.quiz_mode
    )
    db.add(new_quiz)
    db.flush()

    # Копируем вопросы и ответы
    if copy_questions :
        source_questions = crud_question.get_questions_by_quiz(db, source_quiz_id)

        for source_q in source_questions :
            # Копируем вопрос
            new_question = models.Question(
                quiz_id=new_quiz.id,
                answer_type=source_q.answer_type,
                points=source_q.points,
                question_text=source_q.question_text,
                media_url=source_q.media_url,
                time_limit_seconds=source_q.time_limit_seconds,
                order_number=source_q.order_number
            )
            db.add(new_question)
            db.flush()

            # Копируем ответы
            for source_a in source_q.answers :
                new_answer = models.Answer(
                    question_id=new_question.id,
                    answer_text=source_a.answer_text,
                    is_correct=source_a.is_correct,
                    order_number=source_a.order_number
                )
                db.add(new_answer)

    db.commit()
    db.refresh(new_quiz)

    return new_quiz