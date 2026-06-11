import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import UploadFile, HTTPException, status

# Базовые пути
BASE_MEDIA_DIR = "media_files"
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml"}
ALLOWED_AUDIO_TYPES = {"audio/mpeg", "audio/wav", "audio/ogg", "audio/mp4", "audio/webm"}
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/webm", "video/ogg", "video/quicktime"}

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB
MAX_AUDIO_SIZE = 20 * 1024 * 1024  # 20 MB
MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100 MB


def get_media_type_by_mime(mime_type: str) -> str:
    """Определение типа медиа по MIME типу"""
    if mime_type in ALLOWED_IMAGE_TYPES:
        return "image"
    elif mime_type in ALLOWED_AUDIO_TYPES:
        return "audio"
    elif mime_type in ALLOWED_VIDEO_TYPES:
        return "video"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {mime_type}"
        )


def get_max_file_size(media_type: str) -> int:
    """Получение максимального размера файла для типа медиа"""
    sizes = {
        "image": MAX_IMAGE_SIZE,
        "audio": MAX_AUDIO_SIZE,
        "video": MAX_VIDEO_SIZE
    }
    return sizes.get(media_type, MAX_IMAGE_SIZE)


def get_entity_subdir(entity_type: str, media_type: str) -> str:
    """Получение поддиректории для сущности"""
    subdirs = {
        "profile": {
            "image": "profile_image",
            "audio": "profile_audio",
            "video": "profile_video"
        },
        "question": {
            "image": "question_image",
            "audio": "question_audio",
            "video": "question_video"
        },
        "quiz": {
            "image": "quiz_image",
            "audio": "quiz_audio",
            "video": "quiz_video"
        },
        "quiz_": {
            "image": "answer_image",
            "audio": "answer_audio",
            "video": "answer_video"
        }
    }
    return subdirs.get(entity_type, {}).get(media_type, "other")


def generate_unique_filename(original_filename: str) -> str:
    """Генерация уникального имени файла"""
    extension = original_filename.split('.')[-1].lower() if '.' in original_filename else ''
    unique_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}_{unique_id}.{extension}" if extension else f"{timestamp}_{unique_id}"


def save_media_file(
        file: UploadFile,
        entity_type: str,
        entity_id: int,
        media_type: Optional[str] = None
) -> dict:
    """
    Сохранение медиафайла

    Args:
        file: Загруженный файл
        entity_type: Тип сущности (profile/question/quiz/answer)
        entity_id: ID сущности
        media_type: Тип медиа (image/audio/video) - опционально, определится автоматически

    Returns:
        Словарь с информацией о сохраненном файле
    """
    # Определяем тип медиа
    if not media_type:
        media_type = get_media_type_by_mime(file.content_type)

    # Проверяем размер
    max_size = get_max_file_size(media_type)
    file.file.seek(0, 2)  # Перемещаемся в конец файла
    file_size = file.file.tell()
    file.file.seek(0)  # Возвращаемся в начало

    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Max size: {max_size // (1024 * 1024)} MB"
        )

    # Создаем путь для сохранения
    subdir = get_entity_subdir(entity_type, media_type)
    relative_path = Path(entity_type) / subdir / str(entity_id)
    full_path = Path(BASE_MEDIA_DIR) / relative_path

    # Создаем директорию если не существует
    full_path.mkdir(parents=True, exist_ok=True)

    # Генерируем уникальное имя файла
    unique_filename = generate_unique_filename(file.filename)
    file_path = full_path / unique_filename

    # Сохраняем файл
    try:
        with open(file_path, "wb") as buffer:
            content = file.file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )

    # Возвращаем информацию о файле
    return {
        "file_path": str(relative_path / unique_filename),
        "file_name": file.filename,
        "file_size": file_size,
        "mime_type": file.content_type,
        "media_type": media_type,
        "full_path": str(file_path)
    }


def delete_media_file(file_path: str) -> bool:
    """Удаление медиафайла"""
    full_path = Path(BASE_MEDIA_DIR) / file_path
    if full_path.exists():
        full_path.unlink()
        return True
    return False


def delete_entity_media_files(entity_type: str, entity_id: int) -> dict:
    """Удаление всех медиафайлов сущности"""
    deleted_count = 0
    deleted_paths = []

    entity_path = Path(BASE_MEDIA_DIR) / entity_type

    if entity_path.exists():
        for media_type_dir in entity_path.iterdir():
            entity_dir = media_type_dir / str(entity_id)
            if entity_dir.exists():
                for file in entity_dir.iterdir():
                    if file.is_file():
                        deleted_paths.append(str(file))
                        file.unlink()
                        deleted_count += 1
                # Удаляем пустую директорию
                try:
                    entity_dir.rmdir()
                except OSError:
                    pass

    return {
        "deleted_count": deleted_count,
        "deleted_paths": deleted_paths
    }


def get_file_url(file_path: str) -> str:
    """Получение URL для доступа к файлу"""
    return f"/media/{file_path}"


def validate_file_type(file: UploadFile, allowed_types: set) -> bool:
    """Проверка типа файла"""
    return file.content_type in allowed_types
