from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PendingQuizResponse(BaseModel) :
    id: int
    title: str
    category_id: Optional[int]
    description: str
    cover_url: Optional[str]
    quiz_mode: str
    status: str
    author_id: int
    created_at: datetime
    moderated_at: Optional[datetime] = None

    class Config :
        from_attributes = True
