from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.model_statistic import QuizResult
from ..models.model_user import User
from ...app import schemas
from ...app.utils.security import get_password_hash
from datetime import datetime
from typing import Optional, List


def get_user(db: Session, user_id: int) -> Optional[User] :
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_login(db: Session, login: str) -> Optional[User] :
    return db.query(User).filter(User.login == login).first()


def get_user_by_email(db: Session, email: str) -> Optional[User] :
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User] :
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> User :
    hashed_password = get_password_hash(user.password)
    db_user = User(
        nickname=user.nickname,
        login=user.login,
        email=user.email,
        password_hash=hashed_password,
        theme_site=user.theme_site
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[User] :
    db_user = get_user(db, user_id)
    if db_user :
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items() :
            setattr(db_user, field, value)
        db_user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_user)
    return db_user


def update_user_photo(db: Session, user_id: int, photo_url: str) -> Optional[User] :
    db_user = get_user(db, user_id)
    if db_user :
        db_user.photo_profile = photo_url
        db_user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool :
    db_user = get_user(db, user_id)
    if db_user :
        db.delete(db_user)
        db.commit()
        return True
    return False


def get_user_statistics(db: Session, user_id: int) -> dict :
    """Получение статистики пользователя"""
    total_quizzes = db.query(QuizResult).filter(
        QuizResult.user_id == user_id,
        QuizResult.is_completed == True
    ).count()

    avg_score = db.query(func.avg(QuizResult.score)).filter(
        QuizResult.user_id == user_id,
        QuizResult.is_completed == True
    ).scalar() or 0

    total_points = db.query(func.sum(QuizResult.score)).filter(
        QuizResult.user_id == user_id,
        QuizResult.is_completed == True
    ).scalar() or 0

    return {
        "total_quizzes_completed" : total_quizzes,
        "average_score" : float(avg_score),
        "total_points" : float(total_points)
    }