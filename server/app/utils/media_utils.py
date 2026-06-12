import io
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import UploadFile, HTTPException, status

# Базовые пути
BASE_MEDIA_DIR = "media"
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml", "image/bmp", "image/tiff"}
ALLOWED_AUDIO_TYPES = {"audio/mpeg", "audio/wav", "audio/ogg", "audio/mp4", "audio/webm"}
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/webm", "video/ogg", "video/quicktime"}

# Растровые форматы, которые конвертируем в webp (svg и webp — не трогаем)
WEBP_CONVERTIBLE = {"image/jpeg", "image/png", "image/gif", "image/bmp", "image/tiff"}

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB
MAX_AUDIO_SIZE = 20 * 1024 * 1024  # 20 MB
MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100 MB

# Структура хранения:
#   media/
#     question_media/{quest_image,quest_audio,quest_video}
#     quiz_image/
#     quiz_description/
#     profile_image/
SUBDIR_MAP = {
    ("profile", "image"): "profile_image",
    ("question", "image"): "question_media/quest_image",
    ("question", "audio"): "question_media/quest_audio",
    ("question", "video"): "question_media/quest_video",
    ("quiz", "image"): "quiz_image",
    ("quiz_description", "image"): "quiz_description",
}

# Папки по сущности — для удаления всех файлов сущности
ENTITY_FOLDERS = {
    "profile": ["profile_image"],
    "question": [
        "question_media/quest_image",
        "question_media/quest_audio",
        "question_media/quest_video",
    ],
    "quiz": ["quiz_image"],
    "quiz_description": ["quiz_description"],
}


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
    """Относительная папка хранения для сущности и типа медиа"""
    return SUBDIR_MAP.get((entity_type, media_type), "other")


def ensure_media_dirs():
    """Создать структуру папок media/ (вызывается при старте)."""
    for folders in ENTITY_FOLDERS.values():
        for folder in folders:
            (Path(BASE_MEDIA_DIR) / folder).mkdir(parents=True, exist_ok=True)


def _convert_to_webp(content: bytes) -> bytes:
    """Сконвертировать растровое изображение в webp."""
    from PIL import Image  # ленивый импорт: сервер стартует даже без Pillow

    img = Image.open(io.BytesIO(content))
    # webp поддерживает альфу — сохраняем прозрачность где есть
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
    else:
        img = img.convert("RGB")
    out = io.BytesIO()
    img.save(out, format="WEBP", quality=80, method=6)
    return out.getvalue()


def generate_unique_filename(entity_id: int, extension: str) -> str:
    """Уникальное имя файла с id сущности для трассируемости"""
    unique_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ext = f".{extension}" if extension else ""
    return f"{entity_id}_{timestamp}_{unique_id}{ext}"


def save_media_file(
        file: UploadFile,
        entity_type: str,
        entity_id: int,
        media_type: Optional[str] = None
) -> dict:
    """
    Сохранение медиафайла в структуру media/.
    Растровые картинки (jpg/png/gif/bmp/tiff) автоматически конвертируются в webp.
    """
    # Определяем тип медиа
    if not media_type:
        media_type = get_media_type_by_mime(file.content_type)

    # Проверяем размер
    max_size = get_max_file_size(media_type)
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Max size: {max_size // (1024 * 1024)} MB"
        )

    content = file.file.read()
    original_ext = (
        file.filename.rsplit('.', 1)[-1].lower()
        if file.filename and '.' in file.filename else ''
    )

    # Конвертация в webp для растровых картинок
    if media_type == "image" and file.content_type in WEBP_CONVERTIBLE:
        try:
            content = _convert_to_webp(content)
            extension = "webp"
            mime_type = "image/webp"
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image conversion failed: {str(e)}"
            )
    else:
        extension = original_ext
        mime_type = file.content_type

    # Папка хранения
    subdir = get_entity_subdir(entity_type, media_type)
    full_dir = Path(BASE_MEDIA_DIR) / subdir
    full_dir.mkdir(parents=True, exist_ok=True)

    # Имя и путь
    unique_filename = generate_unique_filename(entity_id, extension)
    file_path = full_dir / unique_filename
    relative_path = Path(subdir) / unique_filename

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )

    return {
        "file_path": str(relative_path).replace("\\", "/"),
        "file_name": file.filename,
        "file_size": len(content),
        "mime_type": mime_type,
        "media_type": media_type,
        "full_path": str(file_path)
    }


def delete_media_file(file_path: str) -> bool:
    """Удаление медиафайла по относительному пути"""
    full_path = Path(BASE_MEDIA_DIR) / file_path
    if full_path.exists():
        full_path.unlink()
        return True
    return False


def delete_entity_media_files(entity_type: str, entity_id: int) -> dict:
    """Удаление всех файлов сущности (по префиксу id в папках типа)."""
    deleted_count = 0
    deleted_paths = []
    prefix = f"{entity_id}_"

    for folder in ENTITY_FOLDERS.get(entity_type, []):
        folder_path = Path(BASE_MEDIA_DIR) / folder
        if not folder_path.exists():
            continue
        for f in folder_path.iterdir():
            if f.is_file() and f.name.startswith(prefix):
                deleted_paths.append(str(f))
                f.unlink()
                deleted_count += 1

    return {"deleted_count": deleted_count, "deleted_paths": deleted_paths}


def get_file_url(file_path: str) -> str:
    """URL для доступа к файлу (через /api, чтобы шёл через прокси)"""
    return f"/api/media/{file_path}"


def validate_file_type(file: UploadFile, allowed_types: set) -> bool:
    """Проверка типа файла"""
    return file.content_type in allowed_types
