"""
Сервис для работы с медиафайлами.
Инкапсулирует бизнес-логику и использует CRUD для доступа к данным.
"""
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

from ..crud import crud_media
from ..utils import media_utils
from ..models.model_media import MediaEntity, MediaType


class MediaService:
    """Сервис для работы с медиафайлами"""

    def __init__(self, db: Session):
        self.db = db

    # ========== ЗАГРУЗКА ФАЙЛОВ ==========

    def upload_media(
            self,
            entity_type: str,
            entity_id: int,
            file,
            alt_text: Optional[str] = None
    ) -> Dict:
        """Загрузка медиафайла для сущности"""
        # Проверяем валидность entity_type
        if entity_type not in ["profile", "question", "quiz", "quiz_description"]:
            raise ValueError("Invalid entity type")

        # Сохраняем файл
        file_info = media_utils.save_media_file(file, entity_type, entity_id)

        # Создаем запись в БД
        db_media = crud_media.create_media_record(
            db=self.db,
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

    def upload_multiple_media(
            self,
            entity_type: str,
            entity_id: int,
            files: List
    ) -> List[Dict]:
        """Загрузка нескольких медиафайлов"""
        uploaded_files = []

        for order, file in enumerate(files):
            file_info = media_utils.save_media_file(file, entity_type, entity_id)
            db_media = crud_media.create_media_record(
                db=self.db,
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

        return uploaded_files

    # ========== ПОЛУЧЕНИЕ ФАЙЛОВ ==========

    def get_entity_media(
            self,
            entity_type: str,
            entity_id: int,
            media_type: Optional[str] = None
    ) -> List[Dict]:
        """Получение всех медиафайлов сущности"""
        media_files = crud_media.get_entity_media(
            db=self.db,
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

    # ========== ОБНОВЛЕНИЕ ==========

    def update_media(
            self,
            media_id: int,
            alt_text: Optional[str] = None,
            order_number: Optional[int] = None
    ) -> Optional[Dict]:
        """Обновление метаданных медиафайла"""
        db_media = crud_media.update_media_record(
            db=self.db,
            media_id=media_id,
            alt_text=alt_text,
            order_number=order_number
        )

        if not db_media:
            return None

        return {
            "id": db_media.id,
            "url": db_media.url,
            "alt_text": db_media.alt_text,
            "order_number": db_media.order_number
        }

    # ========== УДАЛЕНИЕ ==========

    def delete_media(self, media_id: int) -> bool:
        """Удаление медиафайла"""
        return crud_media.delete_media_record(self.db, media_id)

    def delete_entity_media(self, entity_type: str, entity_id: int) -> bool:
        """Удаление всех медиафайлов сущности"""
        crud_media.delete_entity_media(
            db=self.db,
            entity_type=MediaEntity(entity_type),
            entity_id=entity_id
        )
        return True
