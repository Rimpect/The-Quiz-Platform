from datetime import datetime
from typing import Optional, Type

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models.model_quiz_result import QuizResult as quiz_result
from ..models.model_user import User
from ..models.model_user import User as user
from ..schemas.schemas_user import UserCreate, UserUpdate
from ..utils.security import get_password_hash


def get_user(db: Session, user_id: int) -> Optional[Type[user]]:
    return db.query(user).filter(user.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[Type[user]]:
    return db.query(user).filter(user.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> [user]:
    return db.query(user).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """Создание обычного пользователя"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        nickname=user.nickname,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    from . import crud_achievement as achievement_crud
    achievement_crud.initialize_user_achievements(db, db_user.id)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[Type[User]]:
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db_user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


def get_user_statistics(db: Session, user_id: int) -> dict:
    """Статистика пользователя"""
    completed = db.query(quiz_result).filter(
        quiz_result.user_id == user_id,
        quiz_result.is_completed == True
    ).all()

    total_quizzes = len(completed)

    percentages = [
        round(r.score / r.max_score * 100, 1)
        for r in completed
        if r.max_score and r.max_score > 0
    ]

    avg_score = round(sum(percentages) / len(percentages), 1) if percentages else 0
    best_result = max(percentages) if percentages else 0

    total_seconds = 0
    for r in completed:
        try:
            total_seconds += r.duration_seconds or 0
        except Exception:
            pass
    total_minutes = round(total_seconds / 60)

    return {
        "total_quizzes_completed": total_quizzes,
        "average_score": avg_score,
        "best_result": best_result,
        "total_minutes": total_minutes,
    }

