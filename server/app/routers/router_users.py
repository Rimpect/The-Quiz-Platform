from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..crud import crud_user as crud_user
from .. import schemas
from ..database.database import get_db
from ..utils.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) :
    """Создание нового пользователя"""
    # Проверка уникальности логина и email
    if crud_user.get_user_by_email(db, user.email) :
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=user)


@router.get("/", response_model=List[schemas.User])
def read_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
) :
    """Получение списка пользователей"""
    if current_user.role == "admin":
        return crud_user.get_users(db, skip=skip, limit=limit)
    else:
        raise HTTPException(status_code=400, detail="No admin rules")


@router.get("/me", response_model=schemas.User)
def read_current_user(current_user: schemas.User = Depends(get_current_user)) :
    """Получение текущего пользователя"""
    return current_user


@router.get("/{user_id}", response_model=schemas.User)
def read_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
) :
    """Получение пользователя по ID"""
    db_user = crud_user.get_user(db, user_id)
    if db_user is None :
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/me", response_model=schemas.User)
def update_current_user(
        user_update: schemas.UserUpdate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
) :
    """Обновление текущего пользователя"""
    return crud_user.update_user(db, current_user.id, user_update)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
) :
    """Удаление текущего пользователя"""
    crud_user.delete_user(db, current_user.id)


@router.get("/me/statistics")
def get_my_statistics(
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
) :
    """Получение статистики текущего пользователя"""
    return crud_user.get_user_statistics(db, current_user.id)



