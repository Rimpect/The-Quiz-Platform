from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..utils import media_utils
from ..services import MediaService

router = APIRouter(prefix="/media", tags=["media"])


def get_media_service(db: Session = Depends(get_db)) -> MediaService:
    """Dependency для получения экземпляра MediaService"""
    return MediaService(db)


# ========== Загрузка файлов ==========
@router.post("/upload/{entity_type}/{entity_id}")
async def upload_media(
        entity_type: str,
        entity_id: int,
        file: UploadFile = File(...),
        alt_text: Optional[str] = Form(None),
        media_service: MediaService = Depends(get_media_service)
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

    try:
        return media_service.upload_media(entity_type, entity_id, file, alt_text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/upload-multiple/{entity_type}/{entity_id}")
async def upload_multiple_media(
        entity_type: str,
        entity_id: int,
        files: List[UploadFile] = File(...),
        media_service: MediaService = Depends(get_media_service)
):
    """Загрузка нескольких медиафайлов"""
    try:
        uploaded_files = media_service.upload_multiple_media(entity_type, entity_id, files)
        return {"uploaded_files": uploaded_files}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


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
        media_service: MediaService = Depends(get_media_service)
):
    """Получение всех медиафайлов сущности"""
    try:
        media_files = media_service.get_entity_media(entity_type, entity_id, media_type)
        return media_files
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== Обновление и удаление ==========
@router.put("/{media_id}")
async def update_media(
        media_id: int,
        alt_text: Optional[str] = None,
        order_number: Optional[int] = None,
        media_service: MediaService = Depends(get_media_service)
):
    """Обновление метаданных медиафайла"""
    updated = media_service.update_media(media_id, alt_text, order_number)

    if not updated:
        raise HTTPException(status_code=404, detail="Media not found")

    return updated


@router.delete("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_media(
        media_id: int,
        media_service: MediaService = Depends(get_media_service)
):
    """Удаление медиафайла"""
    if not media_service.delete_media(media_id):
        raise HTTPException(status_code=404, detail="Media not found")


@router.delete("/entity/{entity_type}/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entity_media(
        entity_type: str,
        entity_id: int,
        media_service: MediaService = Depends(get_media_service)
):
    """Удаление всех медиафайлов сущности"""
    media_service.delete_entity_media(entity_type, entity_id)
