from typing import List

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..schemas.schemas_user import UserCreate, UserResponse, UserUpdate
from ..schemas.schemas_quiz import QuizUpdate
from ..schemas.schemas_response import ResponseFactory
from ..services import user_service
from ..utils.security import get_current_user


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=6)


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Создание пользователя"""
    return user_service.create_user(db, user)


@router.get("", response_model=List[UserResponse])
def read_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Запрос всех пользователей (только для админов)"""
    return user_service.get_users(db, current_user, skip=skip, limit=limit)


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: UserResponse = Depends(get_current_user)):
    """Получение текущего пользователя"""
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Получение пользователя по ID"""
    return user_service.get_user(db, user_id)


@router.put("/me", response_model=UserResponse)
def update_current_user(
        user_update: UserUpdate,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Обновление текущего пользователя"""
    return user_service.update_current_user(db, current_user, user_update)


@router.delete("/me")
def delete_current_user(
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Удаление текущего пользователя"""
    user_service.delete_current_user(db, current_user)
    return ResponseFactory.success(message="Аккаунт удалён")


@router.post("/me/change-password")
def change_password(
        request: PasswordChangeRequest,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Смена пароля текущего пользователя"""
    user_service.change_password(db, current_user, request.current_password, request.new_password)
    return ResponseFactory.success(message="Пароль успешно изменён")


@router.get("/me/statistics")
def get_my_statistics(
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Получение статистики текущего пользователя"""
    return user_service.get_my_statistics(db, current_user)


#  -------------------------Пользовательские квизы

user_quiz_router = APIRouter(prefix="/me/quizzes", tags=["users"])


@user_quiz_router.get("")
def get_my_quizzes(
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Получение всех квизов текущего пользователя"""
    data = user_service.get_my_quizzes(db, current_user)
    return ResponseFactory.success(data=data, message="User quizzes retrieved")


@user_quiz_router.delete("/{quiz_id}")
def delete_my_quiz(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Удаление своего квиза (любого статуса)"""
    user_service.delete_my_quiz(db, current_user, quiz_id)
    return ResponseFactory.success(message="Quiz deleted successfully")


@user_quiz_router.put("/published/{quiz_id}")
def update_my_published_quiz(
        quiz_id: int,
        quiz_update: QuizUpdate,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Редактирование своего опубликованного квиза"""
    data = user_service.update_my_published_quiz(db, current_user, quiz_id, quiz_update)
    return ResponseFactory.success(data=data, message="Quiz updated successfully")


router.include_router(user_quiz_router)
