from datetime import datetime, timedelta

from sqlalchemy.orm import Session, joinedload

from ..crud import crud_quiz, crud_quiz_result as crud_quiz_results, crud_achievement
from ..models.model_quiz_result import QuizResult
from .exceptions import NotFoundError, BadRequestError

def save_quiz_result(db: Session, current_user, quiz_id: int, score: float,
                     max_score: float, duration_seconds: int = 0):
    if not crud_quiz.get_quiz(db, quiz_id):
        raise NotFoundError("Quiz not found")

    completed_at = datetime.utcnow()
    started_at = completed_at - timedelta(seconds=max(duration_seconds, 0))

    result = QuizResult(
        user_id=current_user.id,
        quiz_id=quiz_id,
        score=score,
        max_score=max_score,
        is_completed=True,
        started_at=started_at,
        completed_at=completed_at,
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    newly_unlocked = crud_achievement.check_and_unlock_achievements(db, current_user.id)
    return {"result_id": result.id, "newly_unlocked": newly_unlocked}

def start_quiz(db: Session, current_user, quiz_id: int):
    if not crud_quiz.get_quiz(db, quiz_id):
        raise NotFoundError("Quiz not found")
    return crud_quiz_results.create_quiz_result(db, current_user.id, quiz_id)

def get_my_results(db: Session, current_user, skip: int = 0, limit: int = 100):
    return crud_quiz_results.get_user_quiz_results(db, current_user.id, skip, limit)

def get_my_history(db: Session, current_user, skip: int = 0, limit: int = 50):
    results = (
        db.query(QuizResult)
        .options(joinedload(QuizResult.quiz))
        .filter(QuizResult.user_id == current_user.id, QuizResult.is_completed == True)
        .order_by(QuizResult.completed_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    history = []
    for r in results:
        quiz = r.quiz
        history.append({
            "id": r.id,
            "quiz_id": r.quiz_id,
            "title": quiz.title if quiz else f"Квиз #{r.quiz_id}",
            "category": (quiz.category_ref.category_type if quiz and quiz.category_ref else ""),
            "score": r.score,
            "max_score": r.max_score,
            "percentage": round(r.percentage, 1),
            "total_questions": quiz.total_questions if quiz else 0,
            "completed_at": r.completed_at.isoformat() if r.completed_at else None,
            "duration_seconds": r.duration_seconds,
        })
    return history

def get_quiz_result(db: Session, current_user, result_id: int):
    result = crud_quiz_results.get_quiz_result(db, result_id)
    if not result or result.user_id != current_user.id:
        raise NotFoundError("Result not found")
    if current_user.role != "admin":
        raise BadRequestError("No admin rules")
    return result

def complete_quiz(db: Session, current_user, result_id: int):
    result = crud_quiz_results.get_quiz_result(db, result_id)
    if not result or result.user_id != current_user.id:
        raise NotFoundError("Result not found")
    if result.is_completed:
        raise BadRequestError("Quiz already completed")

    completed = crud_quiz_results.complete_quiz_result(db, result_id)

    try:
        crud_achievement.check_and_unlock_achievements(db, current_user.id)
    except Exception:
        pass

    return completed
