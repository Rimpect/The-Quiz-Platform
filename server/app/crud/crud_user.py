from datetime import datetime
from typing import Optional, Type

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..crud import crud_quiz as quiz_crud
from ..crud import crud_achievement as achievement_crud
from ..database.database import get_db
from ..models.model_quiz_result import QuizResult as quiz_result
from ..models.model_user import User
from ..models.model_user import User as user
from ..schemas.schemas_quiz import QuizResponse, QuizUpdate
from ..schemas.schemas_response import ResponseFactory
from ..schemas.schemas_user import UserCreate, UserUpdate
from ..utils.security import get_current_user, get_password_hash


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


router = APIRouter(prefix="/users/me/quizzes", tags=["users"])


@router.get("/")
def get_my_quizzes(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) :
    """Получение всех квизов текущего пользователя (опубликованные + на модерации)"""
    user_quizzes = quiz_crud.get_user_quizzes(db, current_user.id)

    return ResponseFactory.success(
        data={
            "published" : [QuizResponse.model_validate(q).model_dump() for q in user_quizzes["published"]],
            "pending" : [{
                "id" : p.id,
                "title" : p.title,
                "status" : p.status.value,
                "created_at" : p.created_at.isoformat() if p.created_at else None
            } for p in user_quizzes["pending"]]
        },
        message="User quizzes retrieved"
    )


@router.delete("/published/{quiz_id}")
def delete_my_published_quiz(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) :
    """Удаление своего опубликованного квиза"""
    deleted = quiz_crud.delete_quiz(db, quiz_id, current_user.id, is_admin=False)
    if not deleted :
        return ResponseFactory.not_found(f"Quiz {quiz_id}")

    return ResponseFactory.success(message="Quiz deleted successfully")


@router.delete("/pending/{pending_id}")
def delete_my_pending_quiz(
        pending_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) :
    """Удаление своего квиза из модерации"""
    deleted = quiz_crud.delete_pending_quiz(db, pending_id, current_user.id, is_admin=False)
    if not deleted :
        return ResponseFactory.not_found(f"Pending quiz {pending_id}")

    return ResponseFactory.success(message="Pending quiz deleted successfully")


@router.put("/published/{quiz_id}")
def update_my_published_quiz(
        quiz_id: int,
        quiz_update: QuizUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) :
    """Редактирование своего опубликованного квиза"""
    updated = quiz_crud.update_quiz(db, quiz_id, quiz_update, current_user.id)
    if not updated :
        return ResponseFactory.not_found(f"Quiz {quiz_id}")

    return ResponseFactory.success(
        data=QuizResponse.model_validate(updated).model_dump(),
        message="Quiz updated successfully"
    )

