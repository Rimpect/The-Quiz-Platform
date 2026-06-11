"""
Схемы для лобби и сессий
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class LobbyCreate(BaseModel):
    quiz_id: int
    max_players: int = Field(4, ge=2, le=10)
    is_public: bool = False


class LobbyResponse(BaseModel):
    lobby_id: str
    host_user_id: int
    quiz_id: int
    max_players: int
    status: str  # waiting, playing, finished
    players: List[int]
    created_at: datetime
    started_at: Optional[datetime] = None


class JoinLobbyRequest(BaseModel):
    lobby_id: str


class StartGameResponse(BaseModel):
    lobby_id: str
    status: str
    players: List[int]
    sessions: List[dict]
