from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session


from ..crud import crud_quiz as quiz_crud
from ..crud import crud_user as crud_user
from ..database.database import get_db
from ..schemas.schemas_user import UserRole
from ..schemas.schemas_user import UserCreate, UserResponse, UserUpdate
from ..schemas.schemas_quiz import QuizResponse, QuizUpdate
from ..schemas.schemas_response import ResponseFactory
from ..utils.security import get_current_user, verify_password, get_password_hash


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=6)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Создание пользователя
  param user: шаблон пользователя из схемы
  param db: запрос к базе данных
  return: создан пользователь
    """

    if crud_user.get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Этот email уже зарегистрирован"
        )
    return crud_user.create_user(db=db, user=user)


@router.get("", response_model=List[UserResponse])
def read_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
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


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: UserResponse = Depends(get_current_user)):
    """Получение текущего пользователя"""
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
def read_user(
        user_id: int,
        db: Session = Depends(get_db),
):
    """Получение пользователя по ID"""
    db_user = crud_user.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/me", response_model=UserResponse)
def update_current_user(
        user_update: UserUpdate,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Обновление текущего пользователя"""
    return crud_user.update_user(db, current_user.id, user_update)


@router.delete("/me")
def delete_current_user(
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Удаление текущего пользователя"""
    crud_user.delete_user(db, current_user.id)
    return ResponseFactory.success(message="Аккаунт удалён")


@router.post("/me/change-password")
def change_password(
        request: PasswordChangeRequest,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Смена пароля текущего пользователя"""
    db_user = crud_user.get_user(db, current_user.id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(request.current_password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Неверный текущий пароль")
    db_user.password_hash = get_password_hash(request.new_password)
    db.commit()
    return ResponseFactory.success(message="Пароль успешно изменён")


@router.get("/me/statistics")
def get_my_statistics(
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Получение статистики текущего пользователя"""
    return crud_user.get_user_statistics(db, current_user.id)


#  -------------------------Пользовательские квизы

user_quiz_router = APIRouter(prefix="/me/quizzes", tags=["users"])


@user_quiz_router.get("")
def get_my_quizzes(
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Получение всех квизов текущего пользователя"""
    user_quizzes = quiz_crud.get_user_quizzes(db, current_user.id)

    def serialize(quizzes):
        return [QuizResponse.model_validate(q).model_dump() for q in quizzes]

    return ResponseFactory.success(
        data={
            "approved": serialize(user_quizzes["approved"]),
            "pending": serialize(user_quizzes["pending"]),
            "rejected": serialize(user_quizzes["rejected"]),
        },
        message="User quizzes retrieved"
    )


@user_quiz_router.delete("/{quiz_id}")
def delete_my_quiz(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Удаление своего квиза (любого статуса)"""
    deleted = quiz_crud.delete_quiz(db, quiz_id, current_user.id, is_admin=False)
    if not deleted:
        return ResponseFactory.not_found(f"Quiz {quiz_id}")
    return ResponseFactory.success(message="Quiz deleted successfully")


@user_quiz_router.put("/published/{quiz_id}")
def update_my_published_quiz(
        quiz_id: int,
        quiz_update: QuizUpdate,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
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
