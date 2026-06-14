"""
API для игровых сессий (командные, рейтинговые квизы)
"""
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database.database import get_db
from ..models.model_user import User
from ..utils.security import get_current_user, verify_access_token
from ..schemas.schemas_response import ResponseFactory
from ..game_services.game_sessions_manager import game_sessions_manager, GameMode
from ..game_services.ws_manager import ws_manager
from ..services import GameSessionService, QuizService

router = APIRouter(prefix="/game", tags=["game"])


def get_game_service(db: Session = Depends(get_db)) -> GameSessionService:
    """Dependency для получения экземпляра GameSessionService"""
    return GameSessionService(db)


def get_quiz_service(db: Session = Depends(get_db)) -> QuizService:
    """Dependency для получения экземпляра QuizService"""
    return QuizService(db)


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


class AnsweredRequest(BaseModel):
    question_index: int


class VoteRequest(BaseModel):
    question_index: int
    answer_ids: List[int]  # индексы выбранных вариантов


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
    answer_ids: List[int]  # Могут быть несколько для множественного выбора
    is_correct: bool
    points_earned: int


class FinishGameRequest(BaseModel):
    session_id: str
    final_score: float


# ============ Endpoints ============
@router.post("/sessions/create")
def create_game_session(
    request: CreateSessionRequest,
    game_service: GameSessionService = Depends(get_game_service),
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user: User = Depends(get_current_user),
):
    """Создать новую игровую сессию"""
    quiz = quiz_service.get_quiz(request.quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    try:
        result = game_service.create_game_session(
            quiz_id=request.quiz_id,
            quiz_title=quiz["title"],
            total_questions=quiz.get("total_questions", 0),
            game_mode=request.game_mode,
            user_id=current_user.id,
            user_nickname=current_user.nickname,
            team_id=request.team_id,
            team_name=request.team_name,
        )
        return ResponseFactory.success(
            data={"session_id": result["session_id"]},
            message="Game session created",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/sessions/join")
def join_game_session(
    request: JoinSessionRequest,
    game_service: GameSessionService = Depends(get_game_service),
    current_user: User = Depends(get_current_user),
):
    """Присоединиться к игровой сессии"""
    try:
        state = game_service.join_game_session(
            request.session_id,
            current_user.id,
            current_user.nickname,
        )
        return ResponseFactory.success(data=state, message="Joined game session")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/lobby/join")
def join_lobby(
    request: JoinLobbyRequest,
    game_service: GameSessionService = Depends(get_game_service),
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user: User = Depends(get_current_user),
):
    """Войти в общее лобби квиза: найти открытое лобби или создать новое."""
    quiz = quiz_service.get_quiz(request.quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    try:
        # Найти открытое лобби для этого квиза
        session_id = game_service.find_open_lobby(request.quiz_id, request.game_mode)
        
        if not session_id:
            # Создать новое лобби
            result = game_service.create_lobby(
                quiz_id=request.quiz_id,
                game_mode=request.game_mode,
                user_id=current_user.id,
                user_nickname=current_user.nickname,
                lobby_wait_seconds=quiz.get("lobby_wait_time_seconds", 30),
                max_team_members=quiz.get("max_team_members", 10),
            )
            session_id = result["session_id"]
        else:
            # Присоединиться к существующему
            state = game_service.join_game_session(
                session_id,
                current_user.id,
                current_user.nickname,
                getattr(current_user, "photo_profile", "") or "",
            )
            return ResponseFactory.success(data=state, message="Joined lobby")
        
        state = game_service.get_session_state(session_id, current_user.id)
        return ResponseFactory.success(data=state, message="Joined lobby")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/lobby/create")
def create_lobby(
    request: CreateLobbyRequest,
    game_service: GameSessionService = Depends(get_game_service),
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user: User = Depends(get_current_user),
):
    """Создать новое хост-лобби с кодом приглашения (для командного режима)."""
    quiz = quiz_service.get_quiz(request.quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    try:
        result = game_service.create_lobby(
            quiz_id=request.quiz_id,
            game_mode=request.game_mode,
            user_id=current_user.id,
            user_nickname=current_user.nickname,
            lobby_wait_seconds=request.lobby_wait_seconds or quiz.get("lobby_wait_time_seconds", 30),
            max_team_members=quiz.get("max_team_members", 10),
        )
        state = game_service.get_session_state(result["session_id"], current_user.id)
        return ResponseFactory.success(data=state, message="Lobby created")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/lobby/join-by-code")
def join_by_code(
    request: JoinByCodeRequest,
    game_service: GameSessionService = Depends(get_game_service),
    current_user: User = Depends(get_current_user),
):
    """Войти в лобби по коду приглашения."""
    try:
        state = game_service.join_lobby_by_code(
            request.code,
            current_user.id,
            current_user.nickname,
            getattr(current_user, "photo_profile", "") or "",
        )
        return ResponseFactory.success(data=state, message="Joined lobby by code")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/sessions/{session_id}/leave")
def leave_lobby(
    session_id: str,
    game_service: GameSessionService = Depends(get_game_service),
    current_user: User = Depends(get_current_user),
):
    """Покинуть лобби. Если вышел хост — лобби закрывается для всех."""
    try:
        result = game_service.leave_session(session_id, current_user.id)
        return ResponseFactory.success(
            data={"cancelled": result.get("cancelled", False)}, message="Left lobby"
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/sessions/{session_id}/banned")
def report_banned(
    session_id: str,
    game_service: GameSessionService = Depends(get_game_service),
    current_user: User = Depends(get_current_user),
):
    """Игрок забанен анти-читом. Бан per-player: остальные продолжают,
    даже если забанен хост."""
    try:
        result = game_service.ban_player(session_id, current_user.id)
        return ResponseFactory.success(data={"banned": True}, message="Player banned")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/sessions/{session_id}/teams/create")
def create_team(
    session_id: str,
    request: CreateTeamRequest,
    game_service: GameSessionService = Depends(get_game_service),
    current_user: User = Depends(get_current_user),
):
    """Создать команду в лобби (текущий игрок становится лидером)."""
    try:
        result = game_service.create_team(session_id, current_user.id, request.team_name)
        return ResponseFactory.success(
            data={"team_id": result["team_id"], "state": result["state"]}, message="Team created"
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/sessions/{session_id}/teams/join")
def join_team(
    session_id: str,
    request: JoinTeamRequest,
    game_service: GameSessionService = Depends(get_game_service),
    current_user: User = Depends(get_current_user),
):
    """Присоединиться к существующей команде в лобби."""
    try:
        state = game_service.join_team(session_id, current_user.id, request.team_id)
        return ResponseFactory.success(data=state, message="Joined team")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/sessions/{session_id}/teams/leave")
def leave_team(
    session_id: str,
    game_service: GameSessionService = Depends(get_game_service),
    current_user: User = Depends(get_current_user),
):
    """Покинуть свою команду в лобби."""
    try:
        state = game_service.leave_team(session_id, current_user.id)
        return ResponseFactory.success(data=state, message="Left team")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/sessions/{session_id}/ready")
def set_ready(
    session_id: str,
    game_service: GameSessionService = Depends(get_game_service),
    current_user: User = Depends(get_current_user),
):
    """Отметить текущего игрока готовым. Если все готовы — лобби стартует."""
    try:
        state = game_service.set_player_ready(session_id, current_user.id)
        return ResponseFactory.success(data=state, message="Player ready")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/sessions/{session_id}/answered")
def mark_answered(
    session_id: str,
    request: AnsweredRequest,
    game_service: GameSessionService = Depends(get_game_service),
    current_user: User = Depends(get_current_user),
):
    """Отметить, что текущий игрок ответил на вопрос (для раннего перехода)."""
    try:
        state = game_service.mark_answered(session_id, current_user.id, request.question_index)
        return ResponseFactory.success(data=state, message="Answer marked")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/sessions/{session_id}/vote")
def cast_vote(
    session_id: str,
    request: VoteRequest,
    game_service: GameSessionService = Depends(get_game_service),
    current_user: User = Depends(get_current_user),
):
    """Голос рядового участника команды за варианты (можно переголосовать)."""
    try:
        state = game_service.record_vote(
            session_id, current_user.id, request.question_index, request.answer_ids
        )
        return ResponseFactory.success(data=state, message="Vote recorded")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/sessions/{session_id}/team-answer")
def team_answer(
    session_id: str,
    request: TeamAnswerRequest,
    game_service: GameSessionService = Depends(get_game_service),
    current_user: User = Depends(get_current_user),
):
    """Финальный ответ команды (только лидер): фиксирует ответ и копит счёт."""
    try:
        state = game_service.record_team_answer(
            session_id,
            current_user.id,
            request.question_index,
            request.answer_ids,
            request.points_earned,
            request.max_possible,
            request.is_correct,
        )
        return ResponseFactory.success(data=state, message="Team answer recorded")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/sessions/{session_id}/result")
def record_result(
    session_id: str,
    request: ResultRequest,
    game_service: GameSessionService = Depends(get_game_service),
    current_user: User = Depends(get_current_user),
):
    """Зафиксировать финальный результат игрока в сессии (для таблицы группы)."""
    try:
        result = game_service.record_result(
            session_id,
            current_user.id,
            request.score,
            request.max_score,
            request.correct_count,
            request.duration_seconds,
        )
        return ResponseFactory.success(data=result, message="Result recorded")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/sessions/{session_id}/results")
def get_results(
    session_id: str,
    game_service: GameSessionService = Depends(get_game_service),
    current_user: User = Depends(get_current_user),
):
    """Таблица результатов по сессии (группа, что играла вместе)."""
    results = game_service.get_session_results(session_id)
    if results is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return ResponseFactory.success(data=results, message="Session results")


@router.post("/sessions/{session_id}/start")
def start_lobby(
    session_id: str,
    game_service: GameSessionService = Depends(get_game_service),
    current_user: User = Depends(get_current_user),
):
    """Форс-старт лобби (например, по истечении таймера ожидания)."""
    try:
        state = game_service.start_lobby(session_id)
        return ResponseFactory.success(data=state, message="Lobby started")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/sessions/{session_id}")
def get_session_state(
    session_id: str,
    game_service: GameSessionService = Depends(get_game_service),
    current_user: User = Depends(get_current_user),
):
    """Получить состояние игровой сессии (heartbeat + авто-переход по таймеру)"""
    try:
        state = game_service.get_session_state(session_id, current_user.id)
        return ResponseFactory.success(data=state, message="Session state retrieved")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/answers/submit")
def submit_answer(
    request: SubmitAnswerRequest,
    game_service: GameSessionService = Depends(get_game_service),
    current_user: User = Depends(get_current_user),
):
    """Отправить ответ на вопрос"""
    try:
        result = game_service.record_answer(
            session_id=request.session_id,
            user_id=current_user.id,
            question_id=request.question_id,
            answer_ids=request.answer_ids,
            is_correct=request.is_correct,
            points_earned=request.points_earned,
        )
        return ResponseFactory.success(
            data={
                "answer_recorded": True,
                "can_next_question": True,  # Упрощено для сервиса
            },
            message="Answer submitted",
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/questions/next")
def next_question(
    session_id: str,
    game_service: GameSessionService = Depends(get_game_service),
    current_user: User = Depends(get_current_user),
):
    """Перейти на следующий вопрос (для всех игроков)"""
    try:
        result = game_service.next_question(session_id)
        return ResponseFactory.success(
            data=result.get("state", {}),
            message="Next question" if result.get("has_next") else "Game finished",
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/finish")
def finish_game(
    request: FinishGameRequest,
    game_service: GameSessionService = Depends(get_game_service),
    current_user: User = Depends(get_current_user),
):
    """Завершить игру и сохранить результат"""
    try:
        result = game_service.record_result(
            session_id=request.session_id,
            user_id=current_user.id,
            score=int(request.final_score),
            max_score=int(request.final_score),  # Упрощено
            correct_count=0,
            duration_seconds=0,
        )
        return ResponseFactory.success(
            data={
                "result_id": 0,
                "score": request.final_score,
                "max_score": request.final_score,
                "percentage": 100.0,
            },
            message="Game finished and result saved",
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


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
        # Сразу отправляем актуальное состояние
        state = game_sessions_manager.get_session_state(session_id)
        if state:
            await websocket.send_json(state)

        # Цикл приёма: heartbeat + детект отключения
        while True:
            await websocket.receive_text()
            game_sessions_manager.touch_player(session_id, user_id)
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        ws_manager.disconnect(session_id, websocket)
