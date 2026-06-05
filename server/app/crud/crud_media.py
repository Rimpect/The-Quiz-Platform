from typing import Optional, Type

from sqlalchemy.orm import Session

from ..models.model_media import MediaFile, MediaEntity, MediaType
from ..utils import media_utils


def create_media_record(
        db: Session,
        entity_type: MediaEntity,
        entity_id: int,
        file_info: dict,
        alt_text: Optional[str] = None,
        order_number: int = 0
) -> MediaFile:
    """Создание записи о медиафайле в БД"""
    db_media = MediaFile(
        entity_type=entity_type,
        entity_id=entity_id,
        media_type=file_info["media_type"],
        file_path=file_info["file_path"],
        file_name=file_info["file_name"],
        file_size=file_info["file_size"],
        mime_type=file_info["mime_type"],
        alt_text=alt_text,
        order_number=order_number
    )
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media


def get_media_by_id(db: Session, media_id: int) -> Optional[MediaFile]:
    """Получение медиафайла по ID"""
    return db.query(MediaFile).filter(MediaFile.id == media_id).first()


def get_entity_media(
        db: Session,
        entity_type: MediaEntity,
        entity_id: int,
        media_type: Optional[MediaType] = None
) -> list[Type[MediaFile]]:
    """Получение всех медиафайлов сущности"""
    query = db.query(MediaFile).filter(
        MediaFile.entity_type == entity_type,
        MediaFile.entity_id == entity_id
    )
    if media_type:
        query = query.filter(MediaFile.media_type == media_type)
    return query.order_by(MediaFile.order_number).all()


def get_entity_primary_media(
        db: Session,
        entity_type: MediaEntity,
        entity_id: int,
        media_type: MediaType = MediaType.IMAGE
) -> Optional[MediaFile]:
    """Получение основного медиафайла сущности (первый по порядку)"""
    return db.query(MediaFile).filter(
        MediaFile.entity_type == entity_type,
        MediaFile.entity_id == entity_id,
        MediaFile.media_type == media_type
    ).order_by(MediaFile.order_number).first()


def update_media_record(
        db: Session,
        media_id: int,
        alt_text: Optional[str] = None,
        order_number: Optional[int] = None
) -> Optional[MediaFile]:
    """Обновление записи о медиафайле"""
    db_media = get_media_by_id(db, media_id)
    if db_media:
        if alt_text is not None:
            db_media.alt_text = alt_text
        if order_number is not None:
            db_media.order_number = order_number
        db.commit()
        db.refresh(db_media)
    return db_media


def delete_media_record(db: Session, media_id: int) -> bool:
    """Удаление записи о медиафайле и самого файла"""
    db_media = get_media_by_id(db, media_id)
    if db_media:
        # Удаляем физический файл
        media_utils.delete_media_file(db_media.file_path)
        # Удаляем запись из БД
        db.delete(db_media)
        db.commit()
        return True
    return False


def delete_entity_media(db: Session, entity_type: MediaEntity, entity_id: int) -> int:
    """Удаление всех медиафайлов сущности"""
    media_files = get_entity_media(db, entity_type, entity_id)
    deleted_count = 0

    for media in media_files:
        # Удаляем физические файлы
        media_utils.delete_media_file(media.file_path)
        # Удаляем записи из БД
        db.delete(media)
        deleted_count += 1

    db.commit()
    return deleted_count
