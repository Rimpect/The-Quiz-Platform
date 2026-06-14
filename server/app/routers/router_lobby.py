"""
Роутер для управления приватными лобби (многопользовательские игры)
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models import User
from ..schemas.schemas_response import ResponseFactory
from ..schemas.schemas_lobby import LobbyCreate, LobbyResponse
from ..services import lobby_service
from ..utils.security import get_current_user

router = APIRouter(prefix="/lobby", tags=["lobby"])


@router.post("/create", response_model=LobbyResponse)
def create_lobby(
        lobby_data: LobbyCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Создание приватного лобби (хост создаёт комнату для других игроков)."""
    return lobby_service.create_lobby(db, current_user, lobby_data)


@router.post("/join/{lobby_id}", response_model=LobbyResponse)
def join_lobby(lobby_id: str, current_user: User = Depends(get_current_user)):
    """Присоединение к лобби по ID"""
    return lobby_service.join_lobby(current_user, lobby_id)


@router.post("/leave")
def leave_lobby(current_user: User = Depends(get_current_user)):
    """Выход из текущего лобби"""
    return lobby_service.leave_lobby(current_user)


@router.post("/start")
def start_game(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Начало игры в лобби (только для хоста). Создаёт сессии для всех игроков."""
    return lobby_service.start_game(db, current_user)


@router.get("/info")
def get_lobby_info(current_user: User = Depends(get_current_user)):
    """Получение информации о текущем лобби пользователя"""
    return lobby_service.get_lobby_info(current_user)


@router.get("/list")
def get_active_lobbies():
    """Получение списка активных (открытых) лобби"""
    lobbies = lobby_service.get_active_lobbies()
    return ResponseFactory.success(
        data={"total": len(lobbies), "lobbies": lobbies},
        message=f"Found {len(lobbies)} active lobbies",
    )


@router.get("/public")
def get_public_lobbies(limit: int = 20):
    """Получение списка публичных лобби"""
    lobbies = lobby_service.get_public_lobbies(limit)
    return ResponseFactory.success(
        data={"total": len(lobbies), "lobbies": lobbies},
        message=f"Found {len(lobbies)} public lobbies",
    )


@router.post("/join/public/{lobby_id}")
def join_public_lobby(lobby_id: str):
    """Присоединение к публичному лобби (без кода)"""
    return lobby_service.join_public_lobby(lobby_id)
