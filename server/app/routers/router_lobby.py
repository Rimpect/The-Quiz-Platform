"""
Роутер для управления приватными лобби (многопользовательские игры)
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models
from ..config_redis.redis_service import LobbyService, QuizSessionService
from ..crud import crud_quiz as quiz_crud
from ..database.database import get_db
from ..schemas import ResponseFactory
from ..utils.security import get_current_user

router = APIRouter(prefix="/lobby", tags=["lobby"])

# Сервисы
lobby_service = LobbyService()
quiz_session_service = QuizSessionService()


@router.post("/create", response_model=schemas.LobbyResponse)
def create_lobby(
        lobby_data: schemas.LobbyCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    """
    Создание приватного лобби
    Хост создает комнату, куда могут присоединиться другие игроки
    """
    # Проверяем квиз
    quiz = quiz_crud.get_quiz(db, lobby_data.quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # Проверяем, не в лобби ли уже пользователь
    existing = lobby_service.get_user_lobby(current_user.id)
    if existing:
        raise HTTPException(status_code=400, detail="You are already in a lobby")

    # Создаем лобби
    lobby_id = lobby_service.create_lobby(
        host_user_id=current_user.id,
        quiz_id=lobby_data.quiz_id,
        max_players=lobby_data.max_players,
        is_public=lobby_data.is_public
    )

    return lobby_service.get_lobby(lobby_id)


@router.post("/join/{lobby_id}", response_model=schemas.LobbyResponse)
def join_lobby(
        lobby_id: str,
        # db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    """
    Присоединение к лобби по ID
    """
    # Проверяем существование лобби
    lobby = lobby_service.get_lobby(lobby_id)
    if not lobby:
        raise HTTPException(status_code=404, detail="Lobby not found")

    if lobby.get("status") != "waiting":
        raise HTTPException(status_code=400, detail="Game already started")

    players = lobby.get("players", [])
    if len(players) >= int(lobby.get("max_players", 4)):
        raise HTTPException(status_code=400, detail="Lobby is full")

    # Проверяем, не в лобби ли уже пользователь
    existing = lobby_service.get_user_lobby(current_user.id)
    if existing:
        raise HTTPException(status_code=400, detail="You are already in a lobby")

    # Присоединяемся
    success = lobby_service.join_lobby(lobby_id, current_user.id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot join lobby")

    return lobby_service.get_lobby(lobby_id)


@router.post("/leave")
def leave_lobby(
        # db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    """
    Выход из текущего лобби
    """
    lobby = lobby_service.get_user_lobby(current_user.id)
    if not lobby:
        raise HTTPException(status_code=404, detail="You are not in a lobby")

    lobby_service.leave_lobby(lobby["lobby_id"], current_user.id)
    return {"message": "Left lobby"}


@router.post("/start")
def start_game(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    """
    Начало игры в лобби (только для хоста)
    Создает сессии для всех игроков
    """
    lobby = lobby_service.get_user_lobby(current_user.id)
    if not lobby:
        raise HTTPException(status_code=404, detail="Lobby not found")

    # Проверяем, что хост начинает игру
    if lobby.get("host_user_id") != current_user.id:
        raise HTTPException(status_code=403, detail="Only host can start the game")

    players = lobby.get("players", [])
    if len(players) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 players")

    quiz_id = int(lobby.get("quiz_id"))

    # Получаем вопросы квиза
    questions = quiz_crud.get_quiz_questions(db, quiz_id)
    total_questions = len(questions)

    # Создаем сессии для всех игроков
    sessions = {}
    for player_id in players:
        session_id = quiz_session_service.create_session(
            user_id=player_id,
            quiz_id=quiz_id,
            total_questions=total_questions
        )
        sessions[player_id] = session_id

    # Отмечаем, что игра началась
    lobby_service.start_game(lobby["lobby_id"])

    return {
        "message": "Game started",
        "lobby_id": lobby["lobby_id"],
        "players": players,
        "sessions": sessions,
        "total_questions": total_questions
    }


@router.get("/info")
def get_lobby_info(
        current_user: models.User = Depends(get_current_user)
):
    """Получение информации о текущем лобби пользователя"""
    lobby = lobby_service.get_user_lobby(current_user.id)
    if not lobby:
        raise HTTPException(status_code=404, detail="You are not in a lobby")

    return lobby


@router.get("/list")
def get_active_lobbies():
    """
    Получение списка активных (открытых) лобби
    """
    from ..config_redis.redis_config import get_redis, RedisKeys

    redis_client = get_redis()

    # Ищем все ключи лобби
    pattern = RedisKeys.private_lobby("*")
    lobby_keys = redis_client.keys(pattern)

    active_lobbies = []

    for key in lobby_keys:
        lobby_data = redis_client.hgetall(key)

        # Фильтруем только открытые лобби (статус waiting)
        if lobby_data and lobby_data.get("status") == "waiting":
            players = lobby_data.get("players", "[]")
            import json
            try:
                players_list = json.loads(players)
            except ValueError:
                players_list = []

            active_lobbies.append({
                "lobby_id": lobby_data.get("lobby_id"),
                "host_user_id": int(lobby_data.get("host_user_id", 0)),
                "quiz_id": int(lobby_data.get("quiz_id", 0)),
                "max_players": int(lobby_data.get("max_players", 4)),
                "current_players": len(players_list),
                "players": players_list,
                "created_at": lobby_data.get("created_at"),
                "status": lobby_data.get("status")
            })

    # Сортируем по времени создания (новые первыми)
    active_lobbies.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    return ResponseFactory.success(
        data={
            "total": len(active_lobbies),
            "lobbies": active_lobbies
        },
        message=f"Found {len(active_lobbies)} active lobbies"
    )


@router.get("/public")
def get_public_lobbies(
        limit: int = 20,
) :
    """Получение списка публичных лобби"""
    lobbies = lobby_service.get_public_lobbies(limit)

    return ResponseFactory.success(
        data={
            "total" : len(lobbies),
            "lobbies" : lobbies
        },
        message=f"Found {len(lobbies)} public lobbies"
    )


@router.post("/join/public/{lobby_id}")
def join_public_lobby(
        lobby_id: str
) :
    """Присоединение к публичному лобби (без кода)"""
    lobby = lobby_service.get_lobby(lobby_id)
    if not lobby :
        raise HTTPException(404, "Lobby not found")

    if lobby.get("is_public") != "true" :
        raise HTTPException(400, "This lobby is private")


