from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import model_user as user, model_quiz_result as quiz_result
from ..schemas import schemas_user as schemas
from ..utils.security import get_password_hash


def get_user(db: Session, user_id: int) -> user:
    return db.query(user).filter(user.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> user:
    return db.query(user).filter(user.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> [user]:
    return db.query(user).offset(skip).limit(limit).all()


def create_user(db: Session, schema_user: schemas.UserCreate) -> user:
    """Создание обычного пользователя"""
    hashed_password = get_password_hash(schema_user.password)
    schema_user.password = hashed_password
    db_user = schema_user
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> user:
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
    total_quizzes = db.query(quiz_result).filter(
        quiz_result.user_id == user_id,
        quiz_result.is_completed == True
    ).count()

    avg_score = db.query(func.avg(quiz_result.score)).filter(
        quiz_result.user_id == user_id,
        quiz_result.is_completed == True
    ).scalar() or 0

    return {
        "total_quizzes_completed": total_quizzes,
        "average_score": float(avg_score)
    }
