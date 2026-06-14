from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..services import media_service

router = APIRouter(prefix="/media", tags=["media"])


# ========== Загрузка файлов ==========
@router.post("/upload/{entity_type}/{entity_id}")
async def upload_media(
        entity_type: str,
        entity_id: int,
        file: UploadFile = File(...),
        alt_text: Optional[str] = Form(None),
        db: Session = Depends(get_db)
):
    """Загрузка медиафайла для сущности (entity_type: profile, question, quiz, quiz_description)"""
    return media_service.upload_media(db, entity_type, entity_id, file, alt_text)


@router.post("/upload-multiple/{entity_type}/{entity_id}")
async def upload_multiple_media(
        entity_type: str,
        entity_id: int,
        files: List[UploadFile] = File(...),
        db: Session = Depends(get_db)
):
    """Загрузка нескольких медиафайлов"""
    return media_service.upload_multiple_media(db, entity_type, entity_id, files)


@router.post("/upload-simple")
async def upload_simple(
        target: str = Form(...),
        file: UploadFile = File(...),
):
    """Загрузить файл в нужную папку и вернуть только URL (для сущностей без id)."""
    return media_service.upload_simple(target, file)


# ========== Получение файлов ==========
@router.get("/{file_path:path}")
async def get_media(file_path: str):
    """Получение медиафайла по пути"""
    full_path, media_type = media_service.resolve_media_file(file_path)
    return FileResponse(path=full_path, media_type=media_type)


@router.get("/entity/{entity_type}/{entity_id}")
async def get_entity_media(
        entity_type: str,
        entity_id: int,
        media_type: Optional[str] = None,
        db: Session = Depends(get_db)
):
    """Получение всех медиафайлов сущности"""
    return media_service.get_entity_media(db, entity_type, entity_id, media_type)


# ========== Обновление и удаление ==========
@router.put("/{media_id}")
async def update_media(
        media_id: int,
        alt_text: Optional[str] = None,
        order_number: Optional[int] = None,
        db: Session = Depends(get_db)
):
    """Обновление метаданных медиафайла"""
    return media_service.update_media(db, media_id, alt_text, order_number)


@router.delete("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_media(media_id: int, db: Session = Depends(get_db)):
    """Удаление медиафайла"""
    media_service.delete_media(db, media_id)


@router.delete("/entity/{entity_type}/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entity_media(
        entity_type: str,
        entity_id: int,
        db: Session = Depends(get_db)
):
    """Удаление всех медиафайлов сущности"""
    media_service.delete_entity_media(db, entity_type, entity_id)
