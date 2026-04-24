from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas
from app.utils.security import get_password_hash
from datetime import datetime
from typing import Optional, List


def get_user(db: Session, user_id: int) -> Optional[models.User] :
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_login(db: Session, login: str) -> Optional[models.User] :
    return db.query(models.User).filter(models.User.login == login).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User] :
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User] :
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User :
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
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


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User] :
    db_user = get_user(db, user_id)
    if db_user :
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items() :
            setattr(db_user, field, value)
        db_user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_user)
    return db_user


def update_user_photo(db: Session, user_id: int, photo_url: str) -> Optional[models.User] :
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
    total_quizzes = db.query(models.QuizResult).filter(
        models.QuizResult.user_id == user_id,
        models.QuizResult.is_completed == True
    ).count()

    avg_score = db.query(func.avg(models.QuizResult.score)).filter(
        models.QuizResult.user_id == user_id,
        models.QuizResult.is_completed == True
    ).scalar() or 0

    total_points = db.query(func.sum(models.QuizResult.score)).filter(
        models.QuizResult.user_id == user_id,
        models.QuizResult.is_completed == True
    ).scalar() or 0

    return {
        "total_quizzes_completed" : total_quizzes,
        "average_score" : float(avg_score),
        "total_points" : float(total_points)
    }