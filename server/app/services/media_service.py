from pathlib import Path
from typing import List, Optional

from sqlalchemy.orm import Session

from ..crud import crud_media as media_crud
from ..models.model_media import MediaEntity, MediaType
from ..utils import media_utils
from .exceptions import BadRequestError, NotFoundError

ALLOWED_ENTITY_TYPES = ["profile", "question", "quiz", "quiz_description"]

SIMPLE_TARGETS = {
    "quiz": ("quiz", "image"),
    "quiz_description": ("quiz_description", "image"),
    "profile": ("profile", "image"),
    "question_image": ("question", "image"),
    "question_audio": ("question", "audio"),
    "question_video": ("question", "video"),
}

def upload_media(db: Session, entity_type: str, entity_id: int, file, alt_text: Optional[str] = None):
    if entity_type not in ALLOWED_ENTITY_TYPES:
        raise BadRequestError("Invalid entity type")

    file_info = media_utils.save_media_file(file, entity_type, entity_id)
    db_media = media_crud.create_media_record(
        db=db,
        entity_type=MediaEntity(entity_type),
        entity_id=entity_id,
        file_info=file_info,
        alt_text=alt_text,
    )
    return {
        "id": db_media.id,
        "url": db_media.url,
        "file_name": db_media.file_name,
        "file_size": db_media.file_size,
        "media_type": db_media.media_type,
        "alt_text": db_media.alt_text,
    }

def upload_multiple_media(db: Session, entity_type: str, entity_id: int, files: List):
    uploaded_files = []
    for order, file in enumerate(files):
        file_info = media_utils.save_media_file(file, entity_type, entity_id)
        db_media = media_crud.create_media_record(
            db=db,
            entity_type=MediaEntity(entity_type),
            entity_id=entity_id,
            file_info=file_info,
            order_number=order,
        )
        uploaded_files.append({
            "id": db_media.id,
            "url": db_media.url,
            "file_name": db_media.file_name,
            "order": order,
        })
    return {"uploaded_files": uploaded_files}

def upload_simple(target: str, file):
    if target not in SIMPLE_TARGETS:
        raise BadRequestError(f"Invalid target. Allowed: {list(SIMPLE_TARGETS.keys())}")

    entity_type, media_type = SIMPLE_TARGETS[target]
    file_info = media_utils.save_media_file(file, entity_type, 0, media_type)
    return {
        "url": media_utils.get_file_url(file_info["file_path"]),
        "file_name": file_info["file_name"],
        "media_type": file_info["media_type"],
    }

def resolve_media_file(file_path: str):
    import mimetypes

    full_path = Path(media_utils.BASE_MEDIA_DIR) / file_path
    if not full_path.exists() or not full_path.is_file():
        raise NotFoundError("File not found")

    media_type, _ = mimetypes.guess_type(str(full_path))
    if not media_type:
        media_type = "image/webp" if full_path.suffix.lower() == ".webp" else "application/octet-stream"
    return full_path, media_type

def get_entity_media(db: Session, entity_type: str, entity_id: int, media_type: Optional[str] = None):
    media_files = media_crud.get_entity_media(
        db=db,
        entity_type=MediaEntity(entity_type),
        entity_id=entity_id,
        media_type=MediaType(media_type) if media_type else None,
    )
    return [
        {
            "id": m.id,
            "url": m.url,
            "file_name": m.file_name,
            "file_size": m.file_size,
            "media_type": m.media_type,
            "alt_text": m.alt_text,
            "order_number": m.order_number,
        }
        for m in media_files
    ]

def update_media(db: Session, media_id: int, alt_text: Optional[str] = None, order_number: Optional[int] = None):
    db_media = media_crud.update_media_record(
        db=db, media_id=media_id, alt_text=alt_text, order_number=order_number
    )
    if not db_media:
        raise NotFoundError("Media not found")
    return {
        "id": db_media.id,
        "url": db_media.url,
        "alt_text": db_media.alt_text,
        "order_number": db_media.order_number,
    }

def delete_media(db: Session, media_id: int):
    if not media_crud.delete_media_record(db, media_id):
        raise NotFoundError("Media not found")

def delete_entity_media(db: Session, entity_type: str, entity_id: int):
    media_crud.delete_entity_media(
        db=db, entity_type=MediaEntity(entity_type), entity_id=entity_id
    )
