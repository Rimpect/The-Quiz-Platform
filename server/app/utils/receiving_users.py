from typing import Type

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .security import security, verify_access_token
from ..crud import crud_user as user_crud
from ..crud import crud_guest as guest_crud
from ..database.database import get_db
from ..models import User, Guest


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
) -> Type[User] :
    """Получение текущего пользователя"""
    if not credentials :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    token = credentials.credentials
    verification = verify_access_token(token, db)

    if verification["status"] != "valid" :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=verification.get("error_message", "Invalid token")
        )

    if verification.get("is_guest") :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Guest users cannot access this resource"
        )

    user = user_crud.get_user(db, verification["user_id"])
    if not user :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user

def get_current_guest(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
) -> Guest :
    """Получение текущего гостя"""
    if not credentials :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    token = credentials.credentials
    verification = verify_access_token(token, db)

    if verification["status"] != "valid" :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=verification.get("error_message", "Invalid token")
        )

    if not verification.get("is_guest") :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This endpoint is for guests only"
        )

    guest = guest_crud.get_guest_by_session(db, verification["guest_id"])
    if not guest :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Guest session not found"
        )

    return guest

def get_current_user_or_guest_optional(
        request: Request,
        db: Session = Depends(get_db)
) :
    """Получение текущего пользователя или гостя (опционально)"""
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer ") :
        return None

    token = auth_header.split(" ")[1]
    verification = verify_access_token(token, db)

    if verification["status"] != "valid" :
        return None

    if verification.get("is_guest") :
        return guest_crud.get_guest_by_session(db, verification["guest_id"])
    else :
        return user_crud.get_user(db, verification["user_id"])

