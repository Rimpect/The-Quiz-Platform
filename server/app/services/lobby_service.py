from sqlalchemy.orm import Session

from ..config_redis.redis_service import LobbyService, QuizSessionService
from ..crud import crud_quiz as quiz_crud
from .exceptions import NotFoundError, BadRequestError, ForbiddenError

_lobby = LobbyService()
_quiz_sessions = QuizSessionService()

def create_lobby(db: Session, current_user, lobby_data):
    quiz = quiz_crud.get_quiz(db, lobby_data.quiz_id)
    if not quiz:
        raise NotFoundError("Quiz not found")

    if _lobby.get_user_lobby(current_user.id):
        raise BadRequestError("You are already in a lobby")

    lobby_id = _lobby.create_lobby(
        host_user_id=current_user.id,
        quiz_id=lobby_data.quiz_id,
        max_players=lobby_data.max_players,
        is_public=lobby_data.is_public,
    )
    return _lobby.get_lobby(lobby_id)

def join_lobby(current_user, lobby_id: str):
    lobby = _lobby.get_lobby(lobby_id)
    if not lobby:
        raise NotFoundError("Lobby not found")
    if lobby.get("status") != "waiting":
        raise BadRequestError("Game already started")

    players = lobby.get("players", [])
    if len(players) >= int(lobby.get("max_players", 4)):
        raise BadRequestError("Lobby is full")

    if _lobby.get_user_lobby(current_user.id):
        raise BadRequestError("You are already in a lobby")

    if not _lobby.join_lobby(lobby_id, current_user.id):
        raise BadRequestError("Cannot join lobby")

    return _lobby.get_lobby(lobby_id)

def leave_lobby(current_user):
    lobby = _lobby.get_user_lobby(current_user.id)
    if not lobby:
        raise NotFoundError("You are not in a lobby")
    _lobby.leave_lobby(lobby["lobby_id"], current_user.id)
    return {"message": "Left lobby"}

def start_game(db: Session, current_user):
    lobby = _lobby.get_user_lobby(current_user.id)
    if not lobby:
        raise NotFoundError("Lobby not found")
    if lobby.get("host_user_id") != current_user.id:
        raise ForbiddenError("Only host can start the game")

    players = lobby.get("players", [])
    if len(players) < 2:
        raise BadRequestError("Need at least 2 players")

    quiz_id = int(lobby.get("quiz_id"))
    questions = quiz_crud.get_quiz_questions(db, quiz_id)
    total_questions = len(questions)

    sessions = {}
    for player_id in players:
        sessions[player_id] = _quiz_sessions.create_session(
            user_id=player_id, quiz_id=quiz_id, total_questions=total_questions
        )

    _lobby.start_game(lobby["lobby_id"])
    return {
        "message": "Game started",
        "lobby_id": lobby["lobby_id"],
        "players": players,
        "sessions": sessions,
        "total_questions": total_questions,
    }

def get_lobby_info(current_user):
    lobby = _lobby.get_user_lobby(current_user.id)
    if not lobby:
        raise NotFoundError("You are not in a lobby")
    return lobby

def get_active_lobbies():
    import json
    from ..config_redis.redis_config import get_redis, RedisKeys

    redis_client = get_redis()
    lobby_keys = redis_client.keys(RedisKeys.private_lobby("*"))

    active_lobbies = []
    for key in lobby_keys:
        lobby_data = redis_client.hgetall(key)
        if lobby_data and lobby_data.get("status") == "waiting":
            try:
                players_list = json.loads(lobby_data.get("players", "[]"))
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
                "status": lobby_data.get("status"),
            })

    active_lobbies.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return active_lobbies

def get_public_lobbies(limit: int = 20):
    return _lobby.get_public_lobbies(limit)

def join_public_lobby(lobby_id: str):
    lobby = _lobby.get_lobby(lobby_id)
    if not lobby:
        raise NotFoundError("Lobby not found")
    if lobby.get("is_public") != "true":
        raise BadRequestError("This lobby is private")
