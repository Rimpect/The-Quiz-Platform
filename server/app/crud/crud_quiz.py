from datetime import datetime
from typing import Optional, List, Dict, Any, Type
from typing import Type

from sqlalchemy.orm import Session, joinedload

from ..schemas.schemas_quiz import *
from ..models.model_answer import Answer
from ..models.model_pending_quiz import PendingQuiz, PendingQuizStatus
from ..models.model_question import Question as Quest
from ..models.model_quiz import Quiz
from . import crud_categories


def resolve_category_id(db: Session, category_id: Optional[int], category_name: Optional[str]) -> Optional[int]:
    if category_id:
        return category_id
    if category_name and category_name.strip():
        name = category_name.strip()
        existing = crud_categories.get_category_by_type(db, name)
        if existing:
            return existing.id
        return crud_categories.create_category(db, name).id
    return None


def get_quiz(db: Session, quiz_id: int) -> Optional[Quiz]:
    return db.query(Quiz).filter(Quiz.id == quiz_id).first()


def get_quiz_questions(db: Session, quiz_id):
    return db.query(Quest).filter(quiz_id == Quest.quiz_id)


def create_quiz(db: Session, quiz: QuizCreate) -> Quiz:
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


def update_quiz(db: Session, quiz_id: int, quiz_update: QuizUpdate) -> Optional[Quiz]:
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
        quiz_data: QuizBulkCreate,
        author_id: int,
        status: str = "approved"
) -> Dict[str, Any]:
    """Массовое создание квиза с вопросами и ответами за один запрос"""

    is_public = status == "approved"

    category_id = resolve_category_id(db, quiz_data.category_id, quiz_data.category_name)

    # 1. Создаём квиз
    db_quiz = Quiz(
        title=quiz_data.title,
        category_id=category_id,
        description=quiz_data.description,
        cover_url=quiz_data.cover_url,
        is_public=is_public,
        quiz_mode=quiz_data.quiz_mode,
        difficulty=quiz_data.difficulty,
        status=status,
        author_id=author_id,
        lobby_wait_time_seconds=quiz_data.lobby_wait_time_seconds or 30,
        max_team_members=quiz_data.max_team_members or 10,
    )
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)

    questions_created = 0
    answers_created = 0
    total_seconds = 0

    # 2. Создаём вопросы и ответы
    for q_data in quiz_data.questions:
        db_question = Quest(
            quiz_id=db_quiz.id,
            answer_type=q_data.answer_type,
            points=q_data.points,
            question_text=q_data.question_text,
            question_media_url=q_data.media_url,
            time_limit_seconds=q_data.time_limit_seconds,
        )
        db.add(db_question)
        db.flush()
        questions_created += 1
        total_seconds += q_data.time_limit_seconds or 0

        for ans_idx, a_data in enumerate(q_data.answers):
            db_answer = Answer(
                question_id=db_question.id,
                answer_text=a_data.answer_text,
                is_correct=a_data.is_correct,
                order_number=a_data.order_number or ans_idx,
            )
            db.add(db_answer)
            answers_created += 1

    db.commit()

    return {
        "quiz_id": db_quiz.id,
        "title": db_quiz.title,
        "questions_created": questions_created,
        "answers_created": answers_created,
        "total_time_limit_minutes": total_seconds // 60,
    }

def get_quizzes_by_status(db: Session, status: str, skip: int = 0, limit: int = 100):
    """Получение квизов по статусу модерации"""
    from ..models.model_user import User as UserModel
    return (
        db.query(Quiz)
        .options(joinedload(Quiz.category_ref), joinedload(Quiz.author))
        .filter(Quiz.status == status)
        .order_by(Quiz.created_at.desc())
        .offset(skip).limit(limit).all()
    )


def approve_quiz(db: Session, quiz_id: int, moderator_id: int):
    """Одобрить квиз: is_public=True, status='approved'"""
    quiz = get_quiz(db, quiz_id)
    if not quiz:
        return None
    quiz.is_public = True
    quiz.status = "approved"
    quiz.rejection_reason = None
    db.commit()
    db.refresh(quiz)
    return quiz


def reject_quiz(db: Session, quiz_id: int, moderator_id: int, reason: str = None):
    """Отклонить квиз: status='rejected' + причина для автора"""
    quiz = get_quiz(db, quiz_id)
    if not quiz:
        return None
    quiz.is_public = False
    quiz.status = "rejected"
    quiz.rejection_reason = reason
    db.commit()
    db.refresh(quiz)
    return quiz


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
        query = query.filter(Quiz.is_public == True)

    return query.offset(skip).limit(limit).all()


def can_guest_access_quiz(
        db: Session,
        quiz_id: int
) -> bool:
    quiz = get_quiz(db, quiz_id)
    if not quiz:
        return quiz.is_public and quiz.quiz_mode == "single"


# ========== ОПЕРАЦИИ С ОДОБРЕННЫМИ КВИЗАМИ ==========

def get_quiz(db: Session, quiz_id: int) -> Optional[Quiz]:
    return db.query(Quiz).options(joinedload(Quiz.category_ref)).filter(Quiz.id == quiz_id).first()


def get_quizzes(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None,
        author_id: Optional[int] = None,
        is_public: Optional[bool] = True
) -> list[Type[Quiz]] :
    query = db.query(Quiz).options(joinedload(Quiz.category_ref))

    if category_id:
        query = query.filter(Quiz.category_id == category_id)
    if author_id:
        query = query.filter(Quiz.author_id == author_id)
    if is_public is not None:
        query = query.filter(Quiz.is_public == is_public)

    return query.order_by(Quiz.created_at.desc()).offset(skip).limit(limit).all()


def create_quiz_fast(db: Session, quiz: QuizCreate, author_id: int) -> Quiz:
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


def create_quiz_pending(db: Session, quiz: QuizCreate, author_id: int) -> PendingQuiz:
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


def update_quiz(db: Session, quiz_id: int, quiz_update: QuizUpdate, user_id: int) -> Optional[Quiz]:
    """Обновление квиза (только автор)"""
    db_quiz = get_quiz(db, quiz_id)
    if db_quiz and db_quiz.author_id == user_id:
        update_data = quiz_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_quiz, field, value)
        db_quiz.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_quiz)
    return db_quiz


def delete_quiz(db: Session, quiz_id: int, user_id: int, is_admin: bool = False) -> bool:
    """Удаление квиза (автор или админ)"""
    db_quiz = get_quiz(db, quiz_id)
    if db_quiz and (db_quiz.author_id == user_id or is_admin):
        db.delete(db_quiz)
        db.commit()
        return True
    return False


# ========== ОПЕРАЦИИ С КВИЗАМИ НА МОДЕРАЦИИ ==========

def get_pending_quiz(db: Session, pending_id: int) -> Optional[PendingQuiz]:
    return db.query(PendingQuiz).filter(PendingQuiz.id == pending_id).first()


def get_pending_quizzes(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[PendingQuizStatus] = None,
        author_id: Optional[int] = None
) -> list[Type[PendingQuiz]] :
    query = db.query(PendingQuiz)

    if status:
        query = query.filter(PendingQuiz.status == status)
    if author_id:
        query = query.filter(PendingQuiz.author_id == author_id)

    return query.order_by(PendingQuiz.created_at.desc()).offset(skip).limit(limit).all()


def update_pending_quiz_status(
        db: Session,
        pending_id: int,
        status: PendingQuizStatus,
        moderator_id: int
) -> Optional[PendingQuiz]:
    """Обновление статуса квиза на модерации"""
    pending = get_pending_quiz(db, pending_id)
    if pending:
        pending.status = status
        pending.moderated_at = datetime.utcnow()
        pending.moderated_by = moderator_id
        db.commit()
        db.refresh(pending)
    return pending


def approve_pending_quiz(db: Session, pending_id: int, moderator_id: int) -> Optional[Quiz]:
    """Одобрение квиза: перенос из pending в опубликованные"""
    pending = get_pending_quiz(db, pending_id)
    if not pending or pending.status != PendingQuizStatus.PENDING:
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


def reject_pending_quiz(db: Session, pending_id: int, moderator_id: int) -> bool:
    """Отклонение квиза: удаление из pending"""
    pending = get_pending_quiz(db, pending_id)
    if pending and pending.status == PendingQuizStatus.PENDING:
        pending.status = PendingQuizStatus.REJECTED
        pending.moderated_at = datetime.utcnow()
        pending.moderated_by = moderator_id
        db.commit()
        db.delete(pending)
        db.commit()
        return True
    return False


def delete_pending_quiz(db: Session, pending_id: int, user_id: int, is_admin: bool = False) -> bool:
    """Удаление квиза из модерации (автор или админ)"""
    pending = get_pending_quiz(db, pending_id)
    if pending and (pending.author_id == user_id or is_admin):
        db.delete(pending)
        db.commit()
        return True
    return False


# ========== ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ ==========

def update_quiz_full(
        db: Session,
        quiz_id: int,
        quiz_data: QuizBulkCreate,
        user_id: int,
        is_admin: bool = False,
) -> Optional[Dict[str, Any]]:
    """Полное обновление квиза (заголовок + все вопросы с ответами). Для обычных пользователей сбрасывает статус на pending."""
    db_quiz = get_quiz(db, quiz_id)
    if not db_quiz:
        return None
    if not is_admin and db_quiz.author_id != user_id:
        return None

    new_status = "approved" if is_admin else "pending"
    is_public = new_status == "approved"

    db_quiz.title = quiz_data.title
    db_quiz.description = quiz_data.description
    db_quiz.category_id = resolve_category_id(db, quiz_data.category_id, quiz_data.category_name)
    db_quiz.cover_url = quiz_data.cover_url
    db_quiz.quiz_mode = quiz_data.quiz_mode
    db_quiz.difficulty = quiz_data.difficulty
    db_quiz.status = new_status
    db_quiz.is_public = is_public
    db_quiz.lobby_wait_time_seconds = quiz_data.lobby_wait_time_seconds or 30
    db_quiz.max_team_members = quiz_data.max_team_members or 10
    db_quiz.updated_at = datetime.utcnow()

    # Delete old questions and their answers (cascade via FK ondelete)
    db.query(Quest).filter(Quest.quiz_id == quiz_id).delete(synchronize_session=False)
    db.flush()

    questions_created = 0
    answers_created = 0
    total_seconds = 0

    for q_data in quiz_data.questions:
        db_question = Quest(
            quiz_id=db_quiz.id,
            answer_type=q_data.answer_type,
            points=q_data.points,
            question_text=q_data.question_text,
            question_media_url=q_data.media_url,
            time_limit_seconds=q_data.time_limit_seconds,
        )
        db.add(db_question)
        db.flush()
        questions_created += 1
        total_seconds += q_data.time_limit_seconds or 0

        for ans_idx, a_data in enumerate(q_data.answers):
            db_answer = Answer(
                question_id=db_question.id,
                answer_text=a_data.answer_text,
                is_correct=a_data.is_correct,
                order_number=a_data.order_number or ans_idx,
            )
            db.add(db_answer)
            answers_created += 1

    db.commit()

    return {
        "quiz_id": db_quiz.id,
        "title": db_quiz.title,
        "status": new_status,
        "questions_created": questions_created,
        "answers_created": answers_created,
        "total_time_limit_minutes": total_seconds // 60,
    }


def get_user_quizzes(db: Session, user_id: int) -> Dict[str, Any]:
    """Получение всех квизов пользователя из основной таблицы по статусу"""
    quizzes = (
        db.query(Quiz)
        .options(joinedload(Quiz.category_ref))
        .filter(Quiz.author_id == user_id)
        .order_by(Quiz.created_at.desc())
        .all()
    )
    return {
        "approved": [q for q in quizzes if q.status == "approved"],
        "pending": [q for q in quizzes if q.status == "pending"],
        "rejected": [q for q in quizzes if q.status == "rejected"],
    }


def get_quiz_leaderboard(db: Session, quiz_id: int, limit: int = 100) -> List[Dict[str, Any]]:
    """Получение таблицы лидеров для квиза (по результатам)"""
    try:
        from ..models.model_quiz_result import QuizResult
        from ..models.model_user import User as UserModel

        # Сортируем по лучшему результату (счёт ↓, затем время ↑).
        # Лимит применяем ПОСЛЕ дедупликации, поэтому здесь не ограничиваем.
        results = (
            db.query(QuizResult, UserModel.nickname, UserModel.photo_profile, UserModel.id)
            .join(UserModel, QuizResult.user_id == UserModel.id)
            .filter(QuizResult.quiz_id == quiz_id)
            .order_by(
                QuizResult.score.desc(),
                (QuizResult.completed_at - QuizResult.started_at).asc(),
            )
            .all()
        )

        leaderboard = []
        seen_users = set()
        for result, nickname, photo_profile, user_id in results:
            # Оставляем только лучший результат на пользователя.
            # Так как список уже отсортирован, первое вхождение — лучшее.
            if user_id in seen_users:
                continue
            seen_users.add(user_id)

            if result.max_score and result.max_score > 0:
                percent = int(round((result.score / result.max_score * 100)))
            else:
                percent = 0

            duration = result.duration_seconds or 0
            minutes = duration // 60
            seconds = duration % 60
            time_str = f"{minutes}:{seconds:02d}"

            leaderboard.append({
                "place": len(leaderboard) + 1,
                "user_id": user_id,
                "name": nickname or "Игрок",
                "avatar": photo_profile or "",
                "score": result.score,
                "max_score": result.max_score,
                "percent": percent,
                "time": time_str,
            })

            if len(leaderboard) >= limit:
                break

        return leaderboard
    except Exception as e:
        print(f"Error in get_quiz_leaderboard: {e}")
        return []
