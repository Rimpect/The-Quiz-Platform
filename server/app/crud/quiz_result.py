from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from ..models import models, schemas
from datetime import datetime
from typing import Optional, List


def get_quiz_result(db: Session, result_id: int) -> Optional[models.QuizResult] :
    return db.query(models.QuizResult).filter(models.QuizResult.id == result_id).first()


def get_user_quiz_results(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.QuizResult] :
    return db.query(models.QuizResult).filter(
        models.QuizResult.user_id == user_id
    ).order_by(models.QuizResult.started_at.desc()).offset(skip).limit(limit).all()


def get_quiz_results_by_quiz(db: Session, quiz_id: int, skip: int = 0, limit: int = 100) -> List[models.QuizResult] :
    return db.query(models.QuizResult).filter(
        models.QuizResult.quiz_id == quiz_id
    ).order_by(models.QuizResult.started_at.desc()).offset(skip).limit(limit).all()


def create_quiz_result(db: Session, user_id: int, quiz_id: int) -> models.QuizResult :
    """Создание нового результата при старте квиза"""
    # Получаем максимально возможные баллы
    questions = db.query(models.Question).filter(models.Question.quiz_id == quiz_id).all()
    max_score = sum(q.points for q in questions)

    db_result = models.QuizResult(
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


def update_quiz_result(db: Session, result_id: int, result_update: schemas.QuizResultUpdate) -> Optional[
    models.QuizResult] :
    db_result = get_quiz_result(db, result_id)
    if db_result :
        update_data = result_update.model_dump(exclude_unset=True)
        for field, value in update_data.items() :
            setattr(db_result, field, value)
        db.commit()
        db.refresh(db_result)
    return db_result


def complete_quiz_result(db: Session, result_id: int) -> Optional[models.QuizResult] :
    """Завершение квиза и подсчет итогов"""
    db_result = get_quiz_result(db, result_id)
    if db_result :
        # Считаем сумму баллов из ответов пользователя
        total_score = db.query(func.sum(models.UserAnswer.points_earned)).filter(
            models.UserAnswer.quiz_result_id == result_id
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
        models.QuizResult,
        models.User.nickname,
        models.User.photo_profile
    ).join(
        models.User, models.QuizResult.user_id == models.User.id
    ).filter(
        models.QuizResult.quiz_id == quiz_id,
        models.QuizResult.is_completed == True
    ).order_by(
        models.QuizResult.score.desc(),
        models.QuizResult.completed_at.asc()
    ).limit(limit).all()

    leaderboard = []
    for result, nickname, photo in results :
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
) -> models.UserAnswer :
    """Сохранение ответа пользователя на вопрос"""
    # Получаем вопрос и проверяем правильность
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    is_correct = False
    points_earned = 0

    if question.answer_type == schemas.AnswerType.TEXT :
        # Для текстовых ответов нужно отдельное сравнение
        # Здесь упрощенно - проверяем по answer_id если передан
        if answer_id :
            answer = db.query(models.Answer).filter(
                models.Answer.id == answer_id,
                models.Answer.is_correct == True
            ).first()
            is_correct = answer is not None
    else :
        # Для выбора вариантов
        if answer_id :
            answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
            if answer :
                is_correct = answer.is_correct

    if is_correct :
        points_earned = question.points

    db_answer = models.UserAnswer(
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