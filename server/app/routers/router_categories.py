from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..crud import crud_categories

router = APIRouter(prefix="/categories", tags=["media"])


@router.get("/")
async def get_categories(
        db: Session = Depends(get_db),
        categories_id: int = Depends
) :
    return crud_categories.get_categories(db, categories_id)
