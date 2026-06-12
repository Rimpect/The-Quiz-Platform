"""
API для игровых сессий (командные, рейтинговые квизы)
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database.database import get_db
from ..models.model_user import User
from ..utils.security import get_current_user
from ..schemas.schemas_response import ResponseFactory
from ..services.game_sessions_manager import game_sessions_manager, GameMode
from ..crud import crud_game_sessions as game_crud
from ..crud import crud_quiz as quiz_crud

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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Создать новую игровую сессию"""
    quiz = quiz_crud.get_quiz(db, request.quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    try:
        game_mode = GameMode(request.game_mode)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid game mode")

    # Создать сессию в памяти
    session_id = game_sessions_manager.create_session(
        quiz_id=request.quiz_id,
        quiz_title=quiz.title,
        total_questions=len(quiz.questions),
        game_mode=game_mode,
        team_id=request.team_id,
        team_name=request.team_name,
    )

    # Сохранить в БД
    game_crud.create_game_session(
        db,
        session_id=session_id,
        quiz_id=request.quiz_id,
        game_mode=request.game_mode,
        team_id=request.team_id,
        team_name=request.team_name,
    )

    # Добавить создателя в сессию
    game_sessions_manager.add_player(
        session_id,
        current_user.id,
        current_user.nickname,
    )

    if request.game_mode == "team":
        game_crud.add_team_member(
            db,
            session_id=session_id,
            team_id=request.team_id,
            user_id=current_user.id,
        )

    return ResponseFactory.success(
        data={"session_id": session_id},
        message="Game session created",
    )


@router.post("/sessions/join")
def join_game_session(
    request: JoinSessionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Присоединиться к игровой сессии"""
    session = game_sessions_manager.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.is_finished():
        raise HTTPException(status_code=400, detail="Game session is finished")

    # Добавить игрока
    game_sessions_manager.add_player(
        request.session_id,
        current_user.id,
        current_user.nickname,
    )

    if session.game_mode == GameMode.TEAM:
        game_crud.add_team_member(
            db,
            session_id=request.session_id,
            team_id=session.team_id,
            user_id=current_user.id,
        )

    state = game_sessions_manager.get_session_state(request.session_id)
    return ResponseFactory.success(data=state, message="Joined game session")


@router.post("/lobby/join")
def join_lobby(
    request: JoinLobbyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Войти в общее лобби квиза: найти открытое лобби или создать новое."""
    quiz = quiz_crud.get_quiz(db, request.quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    try:
        game_mode = GameMode(request.game_mode)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid game mode")

    # Найти открытое лобби для этого квиза или создать новое
    session_id = game_sessions_manager.find_open_lobby(request.quiz_id, game_mode)
    if not session_id:
        # Лимиты времени по вопросам — для общего серверного отсчёта
        time_limits = [q.time_limit_seconds for q in quiz.questions]
        session_id = game_sessions_manager.create_session(
            quiz_id=request.quiz_id,
            quiz_title=quiz.title,
            total_questions=len(quiz.questions),
            game_mode=game_mode,
            question_time_limits=time_limits,
            lobby_wait_seconds=getattr(quiz, "lobby_wait_time_seconds", 30) or 30,
            max_team_members=getattr(quiz, "max_team_members", 10) or 10,
        )
        game_crud.create_game_session(
            db,
            session_id=session_id,
            quiz_id=request.quiz_id,
            game_mode=request.game_mode,
        )

    # Добавить игрока с аватаром
    game_sessions_manager.add_player(
        session_id,
        current_user.id,
        current_user.nickname,
        getattr(current_user, "photo_profile", "") or "",
    )

    state = game_sessions_manager.get_session_state(session_id)
    return ResponseFactory.success(data=state, message="Joined lobby")


@router.post("/lobby/create")
def create_lobby(
    request: CreateLobbyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Создать новое хост-лобби с кодом приглашения (для командного режима)."""
    quiz = quiz_crud.get_quiz(db, request.quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    try:
        game_mode = GameMode(request.game_mode)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid game mode")

    time_limits = [q.time_limit_seconds for q in quiz.questions]
    code = game_sessions_manager.generate_join_code()
    # Время ожидания лобби задаёт хост при создании (с клампом 10..600 сек)
    default_wait = getattr(quiz, "lobby_wait_time_seconds", 30) or 30
    wait_seconds = request.lobby_wait_seconds or default_wait
    wait_seconds = max(10, min(600, int(wait_seconds)))
    session_id = game_sessions_manager.create_session(
        quiz_id=request.quiz_id,
        quiz_title=quiz.title,
        total_questions=len(quiz.questions),
        game_mode=game_mode,
        question_time_limits=time_limits,
        lobby_wait_seconds=wait_seconds,
        max_team_members=getattr(quiz, "max_team_members", 10) or 10,
        join_code=code,
    )
    game_crud.create_game_session(
        db,
        session_id=session_id,
        quiz_id=request.quiz_id,
        game_mode=request.game_mode,
    )

    # Назначаем создателя хостом лобби
    host_session = game_sessions_manager.get_session(session_id)
    if host_session:
        host_session.host_id = current_user.id

    game_sessions_manager.add_player(
        session_id,
        current_user.id,
        current_user.nickname,
        getattr(current_user, "photo_profile", "") or "",
    )

    state = game_sessions_manager.get_session_state(session_id)
    return ResponseFactory.success(data=state, message="Lobby created")


@router.post("/lobby/join-by-code")
def join_by_code(
    request: JoinByCodeRequest,
    current_user: User = Depends(get_current_user),
):
    """Войти в лобби по коду приглашения."""
    session_id = game_sessions_manager.find_by_code(request.code)
    if not session_id:
        raise HTTPException(status_code=404, detail="Лобби с таким кодом не найдено или уже началось")

    game_sessions_manager.add_player(
        session_id,
        current_user.id,
        current_user.nickname,
        getattr(current_user, "photo_profile", "") or "",
    )

    state = game_sessions_manager.get_session_state(session_id)
    return ResponseFactory.success(data=state, message="Joined lobby by code")


@router.post("/sessions/{session_id}/leave")
def leave_lobby(
    session_id: str,
    current_user: User = Depends(get_current_user),
):
    """Покинуть лобби. Если вышел хост — лобби закрывается для всех."""
    session = game_sessions_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    cancelled = game_sessions_manager.leave_lobby(session_id, current_user.id)
    return ResponseFactory.success(
        data={"cancelled": cancelled}, message="Left lobby"
    )


@router.post("/sessions/{session_id}/banned")
def report_banned(
    session_id: str,
    current_user: User = Depends(get_current_user),
):
    """Игрок забанен анти-читом. Бан per-player: остальные продолжают,
    даже если забанен хост."""
    session = game_sessions_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    game_sessions_manager.ban_player(session_id, current_user.id)
    return ResponseFactory.success(data={"banned": True}, message="Player banned")


@router.post("/sessions/{session_id}/teams/create")
def create_team(
    session_id: str,
    request: CreateTeamRequest,
    current_user: User = Depends(get_current_user),
):
    """Создать команду в лобби (текущий игрок становится лидером)."""
    session = game_sessions_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    team_id = game_sessions_manager.create_team(
        session_id, current_user.id, request.team_name
    )
    state = game_sessions_manager.get_session_state(session_id)
    return ResponseFactory.success(
        data={"team_id": team_id, "state": state}, message="Team created"
    )


@router.post("/sessions/{session_id}/teams/join")
def join_team(
    session_id: str,
    request: JoinTeamRequest,
    current_user: User = Depends(get_current_user),
):
    """Присоединиться к существующей команде в лобби."""
    session = game_sessions_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    ok = game_sessions_manager.join_team(session_id, current_user.id, request.team_id)
    if not ok:
        raise HTTPException(
            status_code=400, detail="Команда не найдена или заполнена"
        )

    state = game_sessions_manager.get_session_state(session_id)
    return ResponseFactory.success(data=state, message="Joined team")


@router.post("/sessions/{session_id}/teams/leave")
def leave_team(
    session_id: str,
    current_user: User = Depends(get_current_user),
):
    """Покинуть свою команду в лобби."""
    session = game_sessions_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    game_sessions_manager.leave_team(session_id, current_user.id)
    state = game_sessions_manager.get_session_state(session_id)
    return ResponseFactory.success(data=state, message="Left team")


@router.post("/sessions/{session_id}/ready")
def set_ready(
    session_id: str,
    current_user: User = Depends(get_current_user),
):
    """Отметить текущего игрока готовым. Если все готовы — лобби стартует."""
    session = game_sessions_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    game_sessions_manager.set_player_ready(session_id, current_user.id)
    state = game_sessions_manager.get_session_state(session_id)
    return ResponseFactory.success(data=state, message="Player ready")


@router.post("/sessions/{session_id}/answered")
def mark_answered(
    session_id: str,
    request: AnsweredRequest,
    current_user: User = Depends(get_current_user),
):
    """Отметить, что текущий игрок ответил на вопрос (для раннего перехода)."""
    session = game_sessions_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    game_sessions_manager.mark_answered(session_id, current_user.id, request.question_index)
    # Сразу двигаем прогресс — вдруг все уже ответили
    game_sessions_manager.sync_progress(session_id)
    state = game_sessions_manager.get_session_state(session_id)
    return ResponseFactory.success(data=state, message="Answer marked")


@router.post("/sessions/{session_id}/vote")
def cast_vote(
    session_id: str,
    request: VoteRequest,
    current_user: User = Depends(get_current_user),
):
    """Голос рядового участника команды за варианты (можно переголосовать)."""
    session = game_sessions_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    game_sessions_manager.record_vote(
        session_id, current_user.id, request.question_index, request.answer_ids
    )
    state = game_sessions_manager.get_session_state(session_id)
    return ResponseFactory.success(data=state, message="Vote recorded")


@router.post("/sessions/{session_id}/team-answer")
def team_answer(
    session_id: str,
    request: TeamAnswerRequest,
    current_user: User = Depends(get_current_user),
):
    """Финальный ответ команды (только лидер): фиксирует ответ и копит счёт."""
    session = game_sessions_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    game_sessions_manager.record_team_answer(
        session_id,
        current_user.id,
        request.question_index,
        request.answer_ids,
        request.points_earned,
        request.max_possible,
        request.is_correct,
    )
    # Двигаем прогресс — вдруг все лидеры уже ответили
    game_sessions_manager.sync_progress(session_id)
    state = game_sessions_manager.get_session_state(session_id)
    return ResponseFactory.success(data=state, message="Team answer recorded")


@router.post("/sessions/{session_id}/result")
def record_result(
    session_id: str,
    request: ResultRequest,
    current_user: User = Depends(get_current_user),
):
    """Зафиксировать финальный результат игрока в сессии (для таблицы группы)."""
    session = game_sessions_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    game_sessions_manager.record_result(
        session_id,
        current_user.id,
        request.score,
        request.max_score,
        request.correct_count,
        request.duration_seconds,
    )
    return ResponseFactory.success(data={"recorded": True}, message="Result recorded")


@router.get("/sessions/{session_id}/results")
def get_results(
    session_id: str,
    current_user: User = Depends(get_current_user),
):
    """Таблица результатов по сессии (группа, что играла вместе)."""
    results = game_sessions_manager.get_results(session_id)
    if results is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return ResponseFactory.success(data=results, message="Session results")


@router.post("/sessions/{session_id}/start")
def start_lobby(
    session_id: str,
    current_user: User = Depends(get_current_user),
):
    """Форс-старт лобби (например, по истечении таймера ожидания)."""
    session = game_sessions_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    game_sessions_manager.start_lobby(session_id)
    state = game_sessions_manager.get_session_state(session_id)
    return ResponseFactory.success(data=state, message="Lobby started")


@router.get("/sessions/{session_id}")
def get_session_state(
    session_id: str,
    current_user: User = Depends(get_current_user),
):
    """Получить состояние игровой сессии (heartbeat + авто-переход по таймеру)"""
    session = game_sessions_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Heartbeat: этот игрок на связи
    game_sessions_manager.touch_player(session_id, current_user.id)
    # Отвалившиеся (нет heartbeat) — в фазе лобби: хост → отмена, игрок → выход
    game_sessions_manager.check_disconnects(session_id)
    # Двигаем общий прогресс вопросов по серверному таймеру
    game_sessions_manager.sync_progress(session_id)

    state = game_sessions_manager.get_session_state(session_id)
    return ResponseFactory.success(data=state, message="Session state retrieved")


@router.post("/answers/submit")
def submit_answer(
    request: SubmitAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Отправить ответ на вопрос"""
    session = game_sessions_manager.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Записать ответ в памяти
    game_sessions_manager.record_answer(
        session_id=request.session_id,
        user_id=current_user.id,
        question_id=request.question_id,
        answer_ids=request.answer_ids,
        is_correct=request.is_correct,
        points_earned=request.points_earned,
    )

    # Сохранить в БД
    game_crud.save_user_answer(
        db,
        session_id=request.session_id,
        user_id=current_user.id,
        quiz_id=session.quiz_id,
        question_id=request.question_id,
        answer_ids=request.answer_ids,
        is_correct=request.is_correct,
        points_earned=request.points_earned,
        time_spent_seconds=session.get_question_elapsed_seconds(),
        question_order=session.current_question_index,
    )

    # Проверить если ВСЕ игроки ответили или истекло время
    all_answered = all(
        request.question_id in player.answers
        for player in session.players.values()
    )
    time_expired = session.is_time_expired(
        time_limit_seconds=30  # TODO: получить реальное время из вопроса
    )

    can_next = all_answered or time_expired

    return ResponseFactory.success(
        data={
            "answer_recorded": True,
            "can_next_question": can_next,
        },
        message="Answer submitted",
    )


@router.post("/questions/next")
def next_question(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Перейти на следующий вопрос (для всех игроков)"""
    session = game_sessions_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    has_next = game_sessions_manager.next_question(session_id)

    if not has_next:
        game_sessions_manager.end_session(session_id)
        game_crud.end_game_session(db, session_id)

    state = game_sessions_manager.get_session_state(session_id)
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
    session = game_sessions_manager.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Завершить сессию
    game_sessions_manager.end_session(request.session_id)
    game_crud.end_game_session(db, request.session_id)

    # Сохранить результат
    quiz = quiz_crud.get_quiz(db, session.quiz_id)
    max_score = sum(q.points for q in quiz.questions) if quiz.questions else 0

    result = game_crud.save_quiz_result(
        db,
        user_id=current_user.id,
        quiz_id=session.quiz_id,
        score=request.final_score,
        max_score=max_score,
        is_completed=True,
    )

    return ResponseFactory.success(
        data={
            "result_id": result.id,
            "score": result.score,
            "max_score": result.max_score,
            "percentage": result.percentage,
        },
        message="Game finished and result saved",
    )
