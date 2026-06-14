from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..schemas.schemas_user import UserRole
from ..schemas.schemas_user import UserCreate, UserResponse, UserUpdate
from ..schemas.schemas_quiz import QuizResponse, QuizUpdate
from ..utils.security import get_current_user
from ..services import UserService, QuizService


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=6)

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Dependency для получения экземпляра UserService"""
    return UserService(db)


def get_quiz_service(db: Session = Depends(get_db)) -> QuizService:
    """Dependency для получения экземпляра QuizService"""
    return QuizService(db)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    """Создание пользователя"""
    try:
        return user_service.create_user(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.get("", response_model=List[UserResponse])
def read_users(
        skip: int = 0,
        limit: int = 100,
        user_service: UserService = Depends(get_user_service),
        current_user: UserResponse = Depends(get_current_user)
):
    """Запрос всех пользователей (только для админов)"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not admin rules"
        )
    return user_service.get_users(skip=skip, limit=limit)


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: UserResponse = Depends(get_current_user)):
    """Получение текущего пользователя"""
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
def read_user(
        user_id: int,
        user_service: UserService = Depends(get_user_service),
):
    """Получение пользователя по ID"""
    user = user_service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/me", response_model=UserResponse)
def update_current_user(
        user_update: UserUpdate,
        user_service: UserService = Depends(get_user_service),
        current_user: UserResponse = Depends(get_current_user)
):
    """Обновление текущего пользователя"""
    return user_service.update_user(current_user.id, user_update)


@router.delete("/me")
def delete_current_user(
        user_service: UserService = Depends(get_user_service),
        current_user: UserResponse = Depends(get_current_user)
):
    """Удаление текущего пользователя"""
    user_service.delete_user(current_user.id)
    return {"message": "Аккаунт удалён"}


@router.post("/me/change-password")
def change_password(
        request: PasswordChangeRequest,
        user_service: UserService = Depends(get_user_service),
        current_user: UserResponse = Depends(get_current_user)
):
    """Смена пароля текущего пользователя"""
    try:
        user_service.change_password(
            current_user.id,
            request.current_password,
            request.new_password
        )
        return {"message": "Пароль успешно изменён"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me/statistics")
def get_my_statistics(
        user_service: UserService = Depends(get_user_service),
        current_user: UserResponse = Depends(get_current_user)
):
    """Получение статистики текущего пользователя"""
    return user_service.get_user_statistics(current_user.id)


#  -------------------------Пользовательские квизы

user_quiz_router = APIRouter(prefix="/me/quizzes", tags=["users"])


@user_quiz_router.get("")
def get_my_quizzes(
        quiz_service: QuizService = Depends(get_quiz_service),
        current_user: UserResponse = Depends(get_current_user)
):
    """Получение всех квизов текущего пользователя"""
    user_quizzes = quiz_service.get_user_quizzes(current_user.id)

    return {
        "approved": user_quizzes["approved"],
        "pending": user_quizzes["pending"],
        "rejected": user_quizzes["rejected"],
    }


@user_quiz_router.delete("/{quiz_id}")
def delete_my_quiz(
        quiz_id: int,
        quiz_service: QuizService = Depends(get_quiz_service),
        current_user: UserResponse = Depends(get_current_user)
):
    """Удаление своего квиза (любого статуса)"""
    deleted = quiz_service.delete_quiz(quiz_id, current_user.id, current_user.role)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Quiz {quiz_id} not found")
    return {"message": "Quiz deleted successfully"}


@user_quiz_router.put("/published/{quiz_id}")
def update_my_published_quiz(
        quiz_id: int,
        quiz_update: QuizUpdate,
        quiz_service: QuizService = Depends(get_quiz_service),
        current_user: UserResponse = Depends(get_current_user)
):
    """Редактирование своего опубликованного квиза"""
    updated = quiz_service.update_quiz(quiz_id, quiz_update, current_user.id, current_user.role)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Quiz {quiz_id} not found")

    return {
        "data": updated,
        "message": "Quiz updated successfully"
    }


router.include_router(user_quiz_router)