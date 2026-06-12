from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

# from ..schemas import schemas_user
from ..crud import crud_media as media_crud
from ..database.database import get_db
from ..models.model_media import MediaEntity, MediaType
from ..utils import media_utils
# from ..utils.security import get_current_user

router = APIRouter(prefix="/media", tags=["media"])


# ========== Загрузка файлов ==========
@router.post("/upload/{entity_type}/{entity_id}")
async def upload_media(
        entity_type: str,
        entity_id: int,
        file: UploadFile = File(...),
        alt_text: Optional[str] = Form(None),
        # current_user: schemas_user = Depends(get_current_user),
        db: Session = Depends(get_db)
):
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
        "id": db_media.id,
        "url": db_media.url,
        "file_name": db_media.file_name,
        "file_size": db_media.file_size,
        "media_type": db_media.media_type,
        "alt_text": db_media.alt_text
    }


@router.post("/upload-multiple/{entity_type}/{entity_id}")
async def upload_multiple_media(
        entity_type: str,
        entity_id: int,
        files: List[UploadFile] = File(...),
        # current_user: schemas_user = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Загрузка нескольких медиафайлов"""
    uploaded_files = []

    for order, file in enumerate(files):
        file_info = media_utils.save_media_file(file, entity_type, entity_id)
        db_media = media_crud.create_media_record(
            db=db,
            entity_type=MediaEntity(entity_type),
            entity_id=entity_id,
            file_info=file_info,
            order_number=order
        )
        uploaded_files.append({
            "id": db_media.id,
            "url": db_media.url,
            "file_name": db_media.file_name,
            "order": order
        })

    return {"uploaded_files": uploaded_files}


# ========== Простая загрузка (файл -> URL, без привязки к id) ==========
# target: quiz | quiz_description | profile | question_image | question_audio | question_video
SIMPLE_TARGETS = {
    "quiz": ("quiz", "image"),
    "quiz_description": ("quiz_description", "image"),
    "profile": ("profile", "image"),
    "question_image": ("question", "image"),
    "question_audio": ("question", "audio"),
    "question_video": ("question", "video"),
}


@router.post("/upload-simple")
async def upload_simple(
        target: str = Form(...),
        file: UploadFile = File(...),
):
    """Загрузить файл в нужную папку и вернуть только URL.
    Используется при создании сущностей, у которых ещё нет id (квиз/вопрос)."""
    if target not in SIMPLE_TARGETS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid target. Allowed: {list(SIMPLE_TARGETS.keys())}"
        )

    entity_type, media_type = SIMPLE_TARGETS[target]
    file_info = media_utils.save_media_file(file, entity_type, 0, media_type)

    return {
        "url": media_utils.get_file_url(file_info["file_path"]),
        "file_name": file_info["file_name"],
        "media_type": file_info["media_type"],
    }


# ========== Получение файлов ==========
@router.get("/{file_path:path}")
async def get_media(file_path: str):
    """Получение медиафайла по пути"""
    import mimetypes

    full_path = Path(media_utils.BASE_MEDIA_DIR) / file_path

    if not full_path.exists() or not full_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    # Правильный content-type по расширению (важно для audio/video и webp)
    media_type, _ = mimetypes.guess_type(str(full_path))
    if not media_type:
        if full_path.suffix.lower() == ".webp":
            media_type = "image/webp"
        else:
            media_type = "application/octet-stream"

    return FileResponse(path=full_path, media_type=media_type)


@router.get("/entity/{entity_type}/{entity_id}")
async def get_entity_media(
        entity_type: str,
        entity_id: int,
        media_type: Optional[str] = None,
        db: Session = Depends(get_db)
):
    """Получение всех медиафайлов сущности"""
    media_files = media_crud.get_entity_media(
        db=db,
        entity_type=MediaEntity(entity_type),
        entity_id=entity_id,
        media_type=MediaType(media_type) if media_type else None
    )

    return [
        {
            "id": m.id,
            "url": m.url,
            "file_name": m.file_name,
            "file_size": m.file_size,
            "media_type": m.media_type,
            "alt_text": m.alt_text,
            "order_number": m.order_number
        }
        for m in media_files
    ]


# ========== Обновление и удаление ==========
@router.put("/{media_id}")
async def update_media(
        media_id: int,
        alt_text: Optional[str] = None,
        order_number: Optional[int] = None,
        # current_user: schemas_user = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Обновление метаданных медиафайла"""
    db_media = media_crud.update_media_record(
        db=db,
        media_id=media_id,
        alt_text=alt_text,
        order_number=order_number
    )

    if not db_media:
        raise HTTPException(status_code=404, detail="Media not found")

    return {
        "id": db_media.id,
        "url": db_media.url,
        "alt_text": db_media.alt_text,
        "order_number": db_media.order_number
    }


@router.delete("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_media(
        media_id: int,
        # current_user: schemas_user = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Удаление медиафайла"""
    if not media_crud.delete_media_record(db, media_id):
        raise HTTPException(status_code=404, detail="Media not found")


@router.delete("/entity/{entity_type}/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entity_media(
        entity_type: str,
        entity_id: int,
        # current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Удаление всех медиафайлов сущности"""
    media_crud.delete_entity_media(
        db=db,
        entity_type=MediaEntity(entity_type),
        entity_id=entity_id
    )
