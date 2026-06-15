from sqlalchemy.orm import Session

from ..crud import crud_quiz as quiz_crud
from ..crud import crud_user
from ..schemas.schemas_user import UserRole, UserCreate, UserUpdate
from ..schemas.schemas_quiz import QuizResponse, QuizUpdate
from ..utils.security import verify_password, get_password_hash
from .exceptions import ConflictError, NotFoundError, BadRequestError, UnauthorizedError

def create_user(db: Session, user: UserCreate):
    if crud_user.get_user_by_email(db, user.email):
        raise ConflictError("Этот email уже зарегистрирован")
    return crud_user.create_user(db=db, user=user)

def get_users(db: Session, current_user, skip: int = 0, limit: int = 100):
    if current_user.role != UserRole.ADMIN:
        raise UnauthorizedError("Not admin rules")
    return crud_user.get_users(db, skip=skip, limit=limit)

def get_user(db: Session, user_id: int):
    db_user = crud_user.get_user(db, user_id)
    if db_user is None:
        raise NotFoundError("User not found")
    return db_user

def update_current_user(db: Session, current_user, user_update: UserUpdate):
    return crud_user.update_user(db, current_user.id, user_update)

def delete_current_user(db: Session, current_user):
    crud_user.delete_user(db, current_user.id)

def change_password(db: Session, current_user, current_password: str, new_password: str):
    db_user = crud_user.get_user(db, current_user.id)
    if not db_user:
        raise NotFoundError("User not found")
    if not verify_password(current_password, db_user.password_hash):
        raise BadRequestError("Неверный текущий пароль")
    db_user.password_hash = get_password_hash(new_password)
    db.commit()

def get_my_statistics(db: Session, current_user):
    return crud_user.get_user_statistics(db, current_user.id)

def get_my_quizzes(db: Session, current_user):
    user_quizzes = quiz_crud.get_user_quizzes(db, current_user.id)

    def serialize(quizzes):
        return [QuizResponse.model_validate(q).model_dump() for q in quizzes]

    return {
        "approved": serialize(user_quizzes["approved"]),
        "pending": serialize(user_quizzes["pending"]),
        "rejected": serialize(user_quizzes["rejected"]),
    }

def delete_my_quiz(db: Session, current_user, quiz_id: int):
    deleted = quiz_crud.delete_quiz(db, quiz_id, current_user.id, is_admin=False)
    if not deleted:
        raise NotFoundError(f"Quiz {quiz_id}")

def update_my_published_quiz(db: Session, current_user, quiz_id: int, quiz_update: QuizUpdate):
    updated = quiz_crud.update_quiz(db, quiz_id, quiz_update, current_user.id)
    if not updated:
        raise NotFoundError(f"Quiz {quiz_id}")
    return QuizResponse.model_validate(updated).model_dump()
