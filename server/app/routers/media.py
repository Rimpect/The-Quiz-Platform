from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .. import schemas
from ..crud import media as media_crud
from ..database.database import get_db
from ..models.model_media import MediaEntity, MediaType
from ..utils import media_utils
from ..utils.security import get_current_user

router = APIRouter(prefix="/media", tags=["media"])


# ========== Загрузка файлов ==========
@router.post("/upload/{entity_type}/{entity_id}")
async def upload_media(
        entity_type: str,
        entity_id: int,
        file: UploadFile = File(...),
        alt_text: Optional[str] = Form(None),
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)
) :
    """
    Загрузка медиафайла для сущности

    entity_type: profile, question, quiz, quiz_description
    """
    # Проверяем валидность entity_type
    if entity_type not in ["profile", "question", "quiz", "quiz_description"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid entity type"
        )

    # Проверяем права доступа (пользователь может загружать только свои файлы)
    # Здесь нужна дополнительная логика проверки прав

    # Сохраняем файл
    file_info = media_utils.save_media_file(file, entity_type, entity_id)

    # Создаем запись в БД
    db_media = media_crud.create_media_record(
        db=db,
        entity_type=MediaEntity(entity_type),
        entity_id=entity_id,
        file_info=file_info,
        alt_text=alt_text
    )

    return {
        "id" : db_media.id,
        "url" : db_media.url,
        "file_name" : db_media.file_name,
        "file_size" : db_media.file_size,
        "media_type" : db_media.media_type,
        "alt_text" : db_media.alt_text
    }


@router.post("/upload-multiple/{entity_type}/{entity_id}")
async def upload_multiple_media(
        entity_type: str,
        entity_id: int,
        files: List[UploadFile] = File(...),
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)
) :
    """Загрузка нескольких медиафайлов"""
    uploaded_files = []

    for order, file in enumerate(files) :
        file_info = media_utils.save_media_file(file, entity_type, entity_id)
        db_media = media_crud.create_media_record(
            db=db,
            entity_type=MediaEntity(entity_type),
            entity_id=entity_id,
            file_info=file_info,
            order_number=order
        )
        uploaded_files.append({
            "id" : db_media.id,
            "url" : db_media.url,
            "file_name" : db_media.file_name,
            "order" : order
        })

    return {"uploaded_files" : uploaded_files}


# ========== Получение файлов ==========
@router.get("/{file_path:path}")
async def get_media(file_path: str) :
    """Получение медиафайла по пути"""
    full_path = Path(media_utils.BASE_MEDIA_DIR) / file_path

    if not full_path.exists() or not full_path.is_file() :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    return FileResponse(
        path=full_path,
        filename=full_path.name,
        media_type="application/octet-stream"  # Браузер сам определит тип
    )


@router.get("/entity/{entity_type}/{entity_id}")
async def get_entity_media(
        entity_type: str,
        entity_id: int,
        media_type: Optional[str] = None,
        db: Session = Depends(get_db)
) :
    """Получение всех медиафайлов сущности"""
    media_files = media_crud.get_entity_media(
        db=db,
        entity_type=MediaEntity(entity_type),
        entity_id=entity_id,
        media_type=MediaType(media_type) if media_type else None
    )

    return [
        {
            "id" : m.id,
            "url" : m.url,
            "file_name" : m.file_name,
            "file_size" : m.file_size,
            "media_type" : m.media_type,
            "alt_text" : m.alt_text,
            "order_number" : m.order_number
        }
        for m in media_files
    ]


# ========== Обновление и удаление ==========
@router.put("/{media_id}")
async def update_media(
        media_id: int,
        alt_text: Optional[str] = None,
        order_number: Optional[int] = None,
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)
) :
    """Обновление метаданных медиафайла"""
    db_media = media_crud.update_media_record(
        db=db,
        media_id=media_id,
        alt_text=alt_text,
        order_number=order_number
    )

    if not db_media :
        raise HTTPException(status_code=404, detail="Media not found")

    return {
        "id" : db_media.id,
        "url" : db_media.url,
        "alt_text" : db_media.alt_text,
        "order_number" : db_media.order_number
    }


@router.delete("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_media(
        media_id: int,
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)
) :
    """Удаление медиафайла"""
    if not media_crud.delete_media_record(db, media_id) :
        raise HTTPException(status_code=404, detail="Media not found")


@router.delete("/entity/{entity_type}/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entity_media(
        entity_type: str,
        entity_id: int,
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)
) :
    """Удаление всех медиафайлов сущности"""
    media_crud.delete_entity_media(
        db=db,
        entity_type=MediaEntity(entity_type),
        entity_id=entity_id
    )
