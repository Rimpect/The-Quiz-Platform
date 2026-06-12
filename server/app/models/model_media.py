import enum

from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func

from ..database.database import Base


class MediaType(str, enum.Enum):
    """Тип медиафайла"""
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"


class MediaEntity(str, enum.Enum):
    """Сущность, к которой привязан медиафайл"""
    PROFILE = "profile"
    QUESTION = "question"
    QUIZ = "quiz"
    QUIZ_DESCRIPTION = "quiz_description"


class MediaFile(Base):
    """Модель для хранения метаданных медиафайлов"""
    __tablename__ = "media_files"

    id = Column(Integer, primary_key=True, index=True)

    # Связь с сущностью
    entity_type = Column(SQLEnum(MediaEntity), nullable=False)  # profile/question/quiz/answer
    entity_id = Column(Integer, nullable=False, index=True)  # ID связанной записи

    # Тип и путь файла
    media_type = Column(SQLEnum(MediaType), nullable=False)  # image/audio/video
    file_path = Column(String(500), nullable=False)  # Относительный путь к файлу
    file_name = Column(String(255), nullable=False)  # Оригинальное имя файла
    file_size = Column(Integer, nullable=False)  # Размер в байтах
    mime_type = Column(String(100), nullable=False)  # MIME тип (image/jpeg, etc.)

    # Доп. метаданные
    alt_text = Column(String(500), nullable=True)  # Альтернативный текст
    order_number = Column(Integer, default=0, nullable=False)  # Порядок (для нескольких файлов)

    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<MediaFile {self.entity_type}/{self.media_type}: {self.file_name}>"

    @property
    def url(self) -> str:
        """Полный URL для доступа к файлу (через /api, чтобы шёл через прокси)"""
        return f"/api/media/{self.file_path}"

    @property
    def file_extension(self) -> str:
        """Расширение файла"""
        return self.file_name.split('.')[-1].lower() if '.' in self.file_name else ''
