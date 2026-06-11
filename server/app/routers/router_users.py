from typing import List

from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..crud import crud_quiz as quiz_crud
from ..crud import crud_user as crud_user
from ..database.database import get_db
from ..schemas.schemas_user import User, UserRole
from ..schemas.schemas_user import UserCreate, UserResponse, UserUpdate
from ..schemas.schemas_quiz import QuizResponse, QuizUpdate
from ..schemas.schemas_response import ResponseFactory
from ..utils.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Создание пользователя
  param user: шаблон пользователя из схемы
  param db: запрос к базе данных
  return: создан пользователь
    """

    if crud_user.get_user_by_email(db, user.email):
        raise ResponseFactory.unauthorized(
            message="Email is registered",
            access_status="denied"
        )
    return crud_user.create_user(db=db, user=user)


@router.get("/", response_model=List[User])
def read_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Запрос всех пользователей(только для админов)
    """
    if current_user.role == UserRole.ADMIN:
        return crud_user.get_users(db, skip=skip, limit=limit)
    else:
        return ResponseFactory.unauthorized(
            message="Not admin rules",
            access_status="denied"
        )


@router.get("/me", response_model=User)
def read_current_user(current_user: User = Depends(get_current_user)):
    """Получение текущего пользователя"""
    return current_user


@router.get("/{user_id}", response_model=User)
def read_user(
        user_id: int,
        db: Session = Depends(get_db),
):
    """Получение пользователя по ID"""
    db_user = crud_user.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/me", response_model=User)
def update_current_user(
        user_update: UserUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Обновление текущего пользователя"""
    return crud_user.update_user(db, current_user.id, user_update)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Удаление текущего пользователя"""
    crud_user.delete_user(db, current_user.id)


@router.get("/me/statistics")
def get_my_statistics(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получение статистики текущего пользователя"""
    return crud_user.get_user_statistics(db, current_user.id)


#  -------------------------Пользовательские квизы

user_quiz_router = APIRouter(prefix="/me/quizzes", tags=["users"])


@user_quiz_router.get("/")
def get_my_quizzes(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получение всех квизов текущего пользователя (опубликованные + на модерации)"""
    user_quizzes = quiz_crud.get_user_quizzes(db, current_user.id)

    return ResponseFactory.success(
        data={
            "published": [QuizResponse.model_validate(q).model_dump() for q in user_quizzes["published"]],
            "pending": [{
                "id": p.id,
                "title": p.title,
                "status": p.status.value,
                "created_at": p.created_at.isoformat() if p.created_at else None
            } for p in user_quizzes["pending"]]
        },
        message="User quizzes retrieved"
    )


@user_quiz_router.delete("/published/{quiz_id}")
def delete_my_published_quiz(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Удаление своего опубликованного квиза"""
    deleted = quiz_crud.delete_quiz(db, quiz_id, current_user.id, is_admin=False)
    if not deleted:
        return ResponseFactory.not_found(f"Quiz {quiz_id}")

    return ResponseFactory.success(message="Quiz deleted successfully")


@user_quiz_router.delete("/pending/{pending_id}")
def delete_my_pending_quiz(
        pending_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Удаление своего квиза из модерации"""
    deleted = quiz_crud.delete_pending_quiz(db, pending_id, current_user.id, is_admin=False)
    if not deleted:
        return ResponseFactory.not_found(f"Pending quiz {pending_id}")

    return ResponseFactory.success(message="Pending quiz deleted successfully")


@user_quiz_router.put("/published/{quiz_id}")
def update_my_published_quiz(
        quiz_id: int,
        quiz_update: QuizUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Редактирование своего опубликованного квиза"""
    updated = quiz_crud.update_quiz(db, quiz_id, quiz_update, current_user.id)
    if not updated:
        return ResponseFactory.not_found(f"Quiz {quiz_id}")

    return ResponseFactory.success(
        data=QuizResponse.model_validate(updated).model_dump(),
        message="Quiz updated successfully"
    )


router.include_router(user_quiz_router)
