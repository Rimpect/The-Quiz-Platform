from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.model_answer import Answer
from ..models.model_statistic import QuizResult
from ..models.model_question import Question
from ..models.model_user import User
from ..models.model_user_answer import UserAnswer
from ...app import schemas
from datetime import datetime
from typing import Optional, List, Type


def get_quiz_result(db: Session, result_id: int) -> Optional[QuizResult] :
    return db.query(QuizResult).filter(QuizResult.id == result_id).first()


def get_user_quiz_results(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Type[QuizResult]] :
    return db.query(QuizResult).filter(
        QuizResult.user_id == user_id
    ).order_by(QuizResult.started_at.desc()).offset(skip).limit(limit).all()


def get_quiz_results_by_quiz(db: Session, quiz_id: int, skip: int = 0, limit: int = 100) -> list[Type[QuizResult]] :
    return db.query(QuizResult).filter(
        QuizResult.quiz_id == quiz_id
    ).order_by(QuizResult.started_at.desc()).offset(skip).limit(limit).all()


def create_quiz_result(db: Session, user_id: int, quiz_id: int) -> QuizResult :
    """Создание нового результата при старте квиза"""
    # Получаем максимально возможные баллы
    questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
    max_score = sum(q.points for q in questions)

    db_result = QuizResult(
        user_id=user_id,
        quiz_id=quiz_id,
        score=0,
        max_score=max_score,
        is_completed=False,
        started_at=datetime.utcnow()
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


def update_quiz_result(db: Session, result_id: int, result_update: schemas.QuizResultUpdate) -> Optional[QuizResult] :
    db_result = get_quiz_result(db, result_id)
    if db_result :
        update_data = result_update.model_dump(exclude_unset=True)
        for field, value in update_data.items() :
            setattr(db_result, field, value)
        db.commit()
        db.refresh(db_result)
    return db_result


def complete_quiz_result(db: Session, result_id: int) -> Optional[QuizResult] :
    """Завершение квиза и подсчет итогов"""
    db_result = get_quiz_result(db, result_id)
    if db_result :
        # Считаем сумму баллов из ответов пользователя
        total_score = db.query(func.sum(UserAnswer.points_earned)).filter(
            UserAnswer.quiz_result_id == result_id
        ).scalar() or 0

        db_result.score = total_score
        db_result.is_completed = True
        db_result.completed_at = datetime.utcnow()
        db.commit()
        db.refresh(db_result)
    return db_result


def delete_quiz_result(db: Session, result_id: int) -> bool :
    db_result = get_quiz_result(db, result_id)
    if db_result :
        db.delete(db_result)
        db.commit()
        return True
    return False


def get_quiz_leaderboard(db: Session, quiz_id: int, limit: int = 10) -> List[dict] :
    """Получение таблицы лидеров для квиза"""
    results = db.query(
        QuizResult,
        User.nickname,
        User.photo_profile
    ).join(
        User, QuizResult.user_id == User.id
    ).filter(
        QuizResult.quiz_id == quiz_id,
        QuizResult.is_completed == True
    ).order_by(
        QuizResult.score.desc(),
        QuizResult.completed_at.asc()
    ).limit(limit).all()

    leaderboard = []
    for result, nickname, photo in results:
        leaderboard.append({
            "user_id" : result.user_id,
            "nickname" : nickname,
            "photo_profile" : photo,
            "score" : result.score,
            "percentage" : result.percentage,
            "completed_at" : result.completed_at
        })
    return leaderboard


def save_user_answer(
        db: Session,
        quiz_result_id: int,
        question_id: int,
        answer_text: Optional[str] = None,
        answer_id: Optional[int] = None,
        time_spent_seconds: Optional[int] = None
) -> UserAnswer:
    """Сохранение ответа пользователя на вопрос"""
    # Получаем вопрос и проверяем правильность
    question = db.query(Question).filter(Question.id == question_id).first()
    is_correct = False
    points_earned = 0

    if question.answer_type == schemas.AnswerType.TEXT :
        # Для текстовых ответов нужно отдельное сравнение
        # Здесь упрощенно - проверяем по answer_id если передан
        if answer_id :
            answer = db.query(Answer).filter(
                Answer.id == answer_id,
                Answer.is_correct == True
            ).first()
            is_correct = answer is not None
    else :
        # Для выбора вариантов
        if answer_id :
            answer = db.query(Answer).filter(Answer.id == answer_id).first()
            if answer:
                is_correct = answer.is_correct

    if is_correct :
        points_earned = question.points

    db_answer = UserAnswer(
        quiz_result_id=quiz_result_id,
        question_id=question_id,
        answer_text=answer_text,
        answer_id=answer_id,
        is_correct=is_correct,
        points_earned=points_earned,
        time_spent_seconds=time_spent_seconds
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer
