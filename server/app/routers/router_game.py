"""
API для игровых сессий (командные, рейтинговые квизы)
"""
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database.database import get_db
from ..models.model_user import User
from ..utils.security import get_current_user, verify_access_token
from ..schemas.schemas_response import ResponseFactory
from ..services import game_service
from ..services.game_sessions_manager import game_sessions_manager
from ..services.ws_manager import ws_manager

router = APIRouter(prefix="/game", tags=["game"])


# ============ Schemas ============
class CreateSessionRequest(BaseModel):
    quiz_id: int
    game_mode: str  # "solo", "competitive", "team"
    team_id: Optional[str] = None
    team_name: Optional[str] = None


class JoinSessionRequest(BaseModel):
    session_id: str


class JoinLobbyRequest(BaseModel):
    quiz_id: int
    game_mode: str  # "competitive", "team"


class CreateLobbyRequest(BaseModel):
    quiz_id: int
    game_mode: str = "team"
    lobby_wait_seconds: Optional[int] = None


class JoinByCodeRequest(BaseModel):
    code: str
    quiz_id: Optional[int] = None


class AnsweredRequest(BaseModel):
    question_index: int


class VoteRequest(BaseModel):
    question_index: int
    answer_ids: List[int]


class TeamAnswerRequest(BaseModel):
    question_index: int
    answer_ids: List[int]
    points_earned: int
    max_possible: int
    is_correct: bool


class ResultRequest(BaseModel):
    score: int
    max_score: int
    correct_count: int = 0
    duration_seconds: int = 0


class CreateTeamRequest(BaseModel):
    team_name: str


class JoinTeamRequest(BaseModel):
    team_id: str


class SubmitAnswerRequest(BaseModel):
    session_id: str
    question_id: int
    answer_ids: List[int]
    is_correct: bool
    points_earned: int


class FinishGameRequest(BaseModel):
    session_id: str
    final_score: float


# ============ Endpoints ============
@router.post("/sessions/create")
def create_game_session(
    request: CreateSessionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Создать новую игровую сессию"""
    data = game_service.create_game_session(db, current_user, request)
    return ResponseFactory.success(data=data, message="Game session created")


@router.post("/sessions/join")
def join_game_session(
    request: JoinSessionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Присоединиться к игровой сессии"""
    state = game_service.join_game_session(db, current_user, request)
    return ResponseFactory.success(data=state, message="Joined game session")


@router.post("/lobby/join")
def join_lobby(
    request: JoinLobbyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Войти в общее лобби квиза: найти открытое лобби или создать новое."""
    state = game_service.join_lobby(db, current_user, request)
    return ResponseFactory.success(data=state, message="Joined lobby")


@router.post("/lobby/create")
def create_lobby(
    request: CreateLobbyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Создать новое хост-лобби с кодом приглашения (для командного режима)."""
    state = game_service.create_lobby(db, current_user, request)
    return ResponseFactory.success(data=state, message="Lobby created")


@router.post("/lobby/join-by-code")
def join_by_code(
    request: JoinByCodeRequest,
    current_user: User = Depends(get_current_user),
):
    """Войти в лобби по коду приглашения."""
    state = game_service.join_by_code(current_user, request)
    return ResponseFactory.success(data=state, message="Joined lobby by code")


@router.post("/sessions/{session_id}/leave")
def leave_lobby(session_id: str, current_user: User = Depends(get_current_user)):
    """Покинуть лобби. Если вышел хост — лобби закрывается для всех."""
    data = game_service.leave_lobby(current_user, session_id)
    return ResponseFactory.success(data=data, message="Left lobby")


@router.post("/sessions/{session_id}/banned")
def report_banned(session_id: str, current_user: User = Depends(get_current_user)):
    """Игрок забанен анти-читом. Бан per-player: остальные продолжают."""
    data = game_service.report_banned(current_user, session_id)
    return ResponseFactory.success(data=data, message="Player banned")


@router.post("/sessions/{session_id}/teams/create")
def create_team(
    session_id: str,
    request: CreateTeamRequest,
    current_user: User = Depends(get_current_user),
):
    """Создать команду в лобби (текущий игрок становится лидером)."""
    data = game_service.create_team(current_user, session_id, request.team_name)
    return ResponseFactory.success(data=data, message="Team created")


@router.post("/sessions/{session_id}/teams/join")
def join_team(
    session_id: str,
    request: JoinTeamRequest,
    current_user: User = Depends(get_current_user),
):
    """Присоединиться к существующей команде в лобби."""
    state = game_service.join_team(current_user, session_id, request.team_id)
    return ResponseFactory.success(data=state, message="Joined team")


@router.post("/sessions/{session_id}/teams/leave")
def leave_team(session_id: str, current_user: User = Depends(get_current_user)):
    """Покинуть свою команду в лобби."""
    state = game_service.leave_team(current_user, session_id)
    return ResponseFactory.success(data=state, message="Left team")


@router.post("/sessions/{session_id}/ready")
def set_ready(session_id: str, current_user: User = Depends(get_current_user)):
    """Отметить текущего игрока готовым. Если все готовы — лобби стартует."""
    state = game_service.set_ready(current_user, session_id)
    return ResponseFactory.success(data=state, message="Player ready")


@router.post("/sessions/{session_id}/answered")
def mark_answered(
    session_id: str,
    request: AnsweredRequest,
    current_user: User = Depends(get_current_user),
):
    """Отметить, что текущий игрок ответил на вопрос (для раннего перехода)."""
    state = game_service.mark_answered(current_user, session_id, request.question_index)
    return ResponseFactory.success(data=state, message="Answer marked")


@router.post("/sessions/{session_id}/vote")
def cast_vote(
    session_id: str,
    request: VoteRequest,
    current_user: User = Depends(get_current_user),
):
    """Голос рядового участника команды за варианты (можно переголосовать)."""
    state = game_service.cast_vote(current_user, session_id, request.question_index, request.answer_ids)
    return ResponseFactory.success(data=state, message="Vote recorded")


@router.post("/sessions/{session_id}/team-answer")
def team_answer(
    session_id: str,
    request: TeamAnswerRequest,
    current_user: User = Depends(get_current_user),
):
    """Финальный ответ команды (только лидер): фиксирует ответ и копит счёт."""
    state = game_service.team_answer(current_user, session_id, request)
    return ResponseFactory.success(data=state, message="Team answer recorded")


@router.post("/sessions/{session_id}/result")
def record_result(
    session_id: str,
    request: ResultRequest,
    current_user: User = Depends(get_current_user),
):
    """Зафиксировать финальный результат игрока в сессии (для таблицы группы)."""
    data = game_service.record_result(current_user, session_id, request)
    return ResponseFactory.success(data=data, message="Result recorded")


@router.get("/sessions/{session_id}/results")
def get_results(session_id: str, current_user: User = Depends(get_current_user)):
    """Таблица результатов по сессии (группа, что играла вместе)."""
    results = game_service.get_results(session_id)
    return ResponseFactory.success(data=results, message="Session results")


@router.post("/sessions/{session_id}/start")
def start_lobby(session_id: str, current_user: User = Depends(get_current_user)):
    """Форс-старт лобби (например, по истечении таймера ожидания)."""
    state = game_service.start_lobby(current_user, session_id)
    return ResponseFactory.success(data=state, message="Lobby started")


@router.get("/sessions/{session_id}")
def get_session_state(session_id: str, current_user: User = Depends(get_current_user)):
    """Получить состояние игровой сессии (heartbeat + авто-переход по таймеру)"""
    state = game_service.get_session_state(current_user, session_id)
    return ResponseFactory.success(data=state, message="Session state retrieved")


@router.post("/answers/submit")
def submit_answer(
    request: SubmitAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Отправить ответ на вопрос"""
    data = game_service.submit_answer(db, current_user, request)
    return ResponseFactory.success(data=data, message="Answer submitted")


@router.post("/questions/next")
def next_question(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Перейти на следующий вопрос (для всех игроков)"""
    state, has_next = game_service.next_question(db, current_user, session_id)
    return ResponseFactory.success(
        data=state,
        message="Next question" if has_next else "Game finished",
    )


@router.post("/finish")
def finish_game(
    request: FinishGameRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Завершить игру и сохранить результат"""
    data = game_service.finish_game(db, current_user, request)
    return ResponseFactory.success(data=data, message="Game finished and result saved")


# ============ WebSocket ============
@router.websocket("/ws/{session_id}")
async def game_ws(websocket: WebSocket, session_id: str):
    """Канал реального времени для игровой сессии (замена поллинга).

    Аутентификация — JWT в query (?token=...), т.к. браузер не шлёт заголовки
    при WS-рукопожатии. Сервер пушит состояние через фоновый тикер; входящие
    сообщения используются как heartbeat (отметка «в сети»).
    """
    token = websocket.query_params.get("token")
    auth = verify_access_token(token) if token else {"status": "invalid"}
    user_id = auth.get("user_id")
    if auth.get("status") != "valid" or not user_id:
        await websocket.close(code=4401)  # Unauthorized
        return

    session = game_sessions_manager.get_session(session_id)
    if not session:
        await websocket.close(code=4404)  # Not found
        return

    await ws_manager.connect(session_id, websocket)
    game_sessions_manager.touch_player(session_id, user_id)

    try:
        state = game_sessions_manager.get_session_state(session_id)
        if state:
            await websocket.send_json(state)

        while True:
            await websocket.receive_text()
            game_sessions_manager.touch_player(session_id, user_id)
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        ws_manager.disconnect(session_id, websocket)
