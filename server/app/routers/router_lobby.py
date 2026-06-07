"""
Роутер для управления приватными лобби (многопользовательские игры)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models
from ..config_redis.redis_service import LobbyService, QuizSessionService
from ..crud import crud_quiz as quiz_crud
from ..database.database import get_db
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
) :
    """
    Создание приватного лобби
    Хост создает комнату, куда могут присоединиться другие игроки
    """
    # Проверяем квиз
    quiz = quiz_crud.get_quiz(db, lobby_data.quiz_id)
    if not quiz :
        raise HTTPException(status_code=404, detail="Quiz not found")

    # Проверяем, не в лобби ли уже пользователь
    existing = lobby_service.get_user_lobby(current_user.id)
    if existing :
        raise HTTPException(status_code=400, detail="You are already in a lobby")

    # Создаем лобби
    lobby_id = lobby_service.create_lobby(
        host_user_id=current_user.id,
        quiz_id=lobby_data.quiz_id,
        max_players=lobby_data.max_players
    )

    return lobby_service.get_lobby(lobby_id)


@router.post("/join/{lobby_id}", response_model=schemas.LobbyResponse)
def join_lobby(
        lobby_id: str,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
) :
    """
    Присоединение к лобби по ID
    """
    # Проверяем существование лобби
    lobby = lobby_service.get_lobby(lobby_id)
    if not lobby :
        raise HTTPException(status_code=404, detail="Lobby not found")

    if lobby.get("status") != "waiting" :
        raise HTTPException(status_code=400, detail="Game already started")

    players = lobby.get("players", [])
    if len(players) >= int(lobby.get("max_players", 4)) :
        raise HTTPException(status_code=400, detail="Lobby is full")

    # Проверяем, не в лобби ли уже пользователь
    existing = lobby_service.get_user_lobby(current_user.id)
    if existing :
        raise HTTPException(status_code=400, detail="You are already in a lobby")

    # Присоединяемся
    success = lobby_service.join_lobby(lobby_id, current_user.id)
    if not success :
        raise HTTPException(status_code=400, detail="Cannot join lobby")

    return lobby_service.get_lobby(lobby_id)


@router.post("/leave")
def leave_lobby(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
) :
    """
    Выход из текущего лобби
    """
    lobby = lobby_service.get_user_lobby(current_user.id)
    if not lobby :
        raise HTTPException(status_code=404, detail="You are not in a lobby")

    lobby_service.leave_lobby(lobby["lobby_id"], current_user.id)
    return {"message" : "Left lobby"}


@router.post("/start")
def start_game(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
) :
    """
    Начало игры в лобби (только для хоста)
    Создает сессии для всех игроков
    """
    lobby = lobby_service.get_user_lobby(current_user.id)
    if not lobby :
        raise HTTPException(status_code=404, detail="Lobby not found")

    # Проверяем, что хост начинает игру
    if lobby.get("host_user_id") != current_user.id :
        raise HTTPException(status_code=403, detail="Only host can start the game")

    players = lobby.get("players", [])
    if len(players) < 2 :
        raise HTTPException(status_code=400, detail="Need at least 2 players")

    quiz_id = int(lobby.get("quiz_id"))

    # Получаем вопросы квиза
    questions = quiz_crud.get_quiz_questions(db, quiz_id)
    total_questions = len(questions)

    # Создаем сессии для всех игроков
    sessions = {}
    for player_id in players :
        session_id = quiz_session_service.create_session(
            user_id=player_id,
            quiz_id=quiz_id,
            total_questions=total_questions
        )
        sessions[player_id] = session_id

    # Отмечаем, что игра началась
    lobby_service.start_game(lobby["lobby_id"])

    return {
        "message" : "Game started",
        "lobby_id" : lobby["lobby_id"],
        "players" : players,
        "sessions" : sessions,
        "total_questions" : total_questions
    }


@router.get("/info")
def get_lobby_info(
        current_user: models.User = Depends(get_current_user)
) :
    """Получение информации о текущем лобби пользователя"""
    lobby = lobby_service.get_user_lobby(current_user.id)
    if not lobby :
        raise HTTPException(status_code=404, detail="You are not in a lobby")

    return lobby


@router.get("/list")
def get_active_lobbies() :
    """Получение списка активных лобби"""
    # В реальном коде нужно получать все активные лобби из Redis
    return {"message" : "Feature: list active lobbies"}