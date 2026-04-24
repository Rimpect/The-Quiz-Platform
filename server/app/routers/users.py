from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db
from app.utils.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Создание нового пользователя"""
    # Проверка уникальности логина и email
    if crud.get_user_by_login(db, user.login):
        raise HTTPException(status_code=400, detail="Login already registered")
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Получение списка пользователей (только для админов)"""
    # Здесь можно добавить проверку на роль admin
    return crud.get_users(db, skip=skip, limit=limit)

@router.get("/me", response_model=schemas.User)
def read_current_user(current_user: schemas.User = Depends(get_current_user)):
    """Получение текущего пользователя"""
    return current_user

@router.get("/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Получение пользователя по ID"""
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/me", response_model=schemas.User)
def update_current_user(
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Обновление текущего пользователя"""
    return crud.update_user(db, current_user.id, user_update)

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Удаление текущего пользователя"""
    crud.delete_user(db, current_user.id)

@router.get("/me/statistics")
def get_my_statistics(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Получение статистики текущего пользователя"""
    return crud.get_user_statistics(db, current_user.id)