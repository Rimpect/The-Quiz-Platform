"""Бизнес-логика игровых сессий (командные/рейтинговые квизы).

HTTP-агностична. Оркестрирует in-memory менеджер (game_sessions_manager),
persistence (game_crud) и проверки; данные возвращает, ошибки кидает доменно.
WebSocket-канал остаётся в роутере (транспортный слой).
"""
from sqlalchemy.orm import Session

from ..crud import crud_game_sessions as game_crud
from ..crud import crud_quiz as quiz_crud
from ..services.game_sessions_manager import game_sessions_manager, GameMode
from .exceptions import NotFoundError, BadRequestError


def _require_session(session_id: str):
    session = game_sessions_manager.get_session(session_id)
    if not session:
        raise NotFoundError("Session not found")
    return session


def _parse_mode(game_mode: str) -> GameMode:
    try:
        return GameMode(game_mode)
    except ValueError:
        raise BadRequestError("Invalid game mode")


def create_game_session(db: Session, current_user, request):
    quiz = quiz_crud.get_quiz(db, request.quiz_id)
    if not quiz:
        raise NotFoundError("Quiz not found")

    game_mode = _parse_mode(request.game_mode)

    session_id = game_sessions_manager.create_session(
        quiz_id=request.quiz_id,
        quiz_title=quiz.title,
        total_questions=len(quiz.questions),
        game_mode=game_mode,
        team_id=request.team_id,
        team_name=request.team_name,
    )
    game_crud.create_game_session(
        db, session_id=session_id, quiz_id=request.quiz_id,
        game_mode=request.game_mode, team_id=request.team_id, team_name=request.team_name,
    )
    game_sessions_manager.add_player(session_id, current_user.id, current_user.nickname)

    if request.game_mode == "team":
        game_crud.add_team_member(
            db, session_id=session_id, team_id=request.team_id, user_id=current_user.id
        )
    return {"session_id": session_id}


def join_game_session(db: Session, current_user, request):
    session = _require_session(request.session_id)
    if session.is_finished():
        raise BadRequestError("Game session is finished")

    game_sessions_manager.add_player(request.session_id, current_user.id, current_user.nickname)
    if session.game_mode == GameMode.TEAM:
        game_crud.add_team_member(
            db, session_id=request.session_id, team_id=session.team_id, user_id=current_user.id
        )
    return game_sessions_manager.get_session_state(request.session_id)


def join_lobby(db: Session, current_user, request):
    quiz = quiz_crud.get_quiz(db, request.quiz_id)
    if not quiz:
        raise NotFoundError("Quiz not found")
    game_mode = _parse_mode(request.game_mode)

    session_id = game_sessions_manager.find_open_lobby(request.quiz_id, game_mode)
    if not session_id:
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
            db, session_id=session_id, quiz_id=request.quiz_id, game_mode=request.game_mode
        )

    game_sessions_manager.add_player(
        session_id, current_user.id, current_user.nickname,
        getattr(current_user, "photo_profile", "") or "",
    )
    return game_sessions_manager.get_session_state(session_id)


def create_lobby(db: Session, current_user, request):
    quiz = quiz_crud.get_quiz(db, request.quiz_id)
    if not quiz:
        raise NotFoundError("Quiz not found")
    game_mode = _parse_mode(request.game_mode)

    time_limits = [q.time_limit_seconds for q in quiz.questions]
    code = game_sessions_manager.generate_join_code()
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
        db, session_id=session_id, quiz_id=request.quiz_id, game_mode=request.game_mode
    )

    host_session = game_sessions_manager.get_session(session_id)
    if host_session:
        host_session.host_id = current_user.id

    game_sessions_manager.add_player(
        session_id, current_user.id, current_user.nickname,
        getattr(current_user, "photo_profile", "") or "",
    )
    return game_sessions_manager.get_session_state(session_id)


def join_by_code(current_user, request):
    session_id = game_sessions_manager.find_by_code(request.code)
    if not session_id:
        raise NotFoundError("Лобби с таким кодом не найдено или уже началось")

    session = game_sessions_manager.get_session(session_id)
    if request.quiz_id is not None and session and session.quiz_id != request.quiz_id:
        raise BadRequestError("Этот код относится к другому квизу")

    game_sessions_manager.add_player(
        session_id, current_user.id, current_user.nickname,
        getattr(current_user, "photo_profile", "") or "",
    )
    return game_sessions_manager.get_session_state(session_id)


def leave_lobby(current_user, session_id: str):
    _require_session(session_id)
    cancelled = game_sessions_manager.leave_lobby(session_id, current_user.id)
    return {"cancelled": cancelled}


def report_banned(current_user, session_id: str):
    _require_session(session_id)
    game_sessions_manager.ban_player(session_id, current_user.id)
    return {"banned": True}


def create_team(current_user, session_id: str, team_name: str):
    _require_session(session_id)
    team_id = game_sessions_manager.create_team(session_id, current_user.id, team_name)
    state = game_sessions_manager.get_session_state(session_id)
    return {"team_id": team_id, "state": state}


def join_team(current_user, session_id: str, team_id: str):
    _require_session(session_id)
    ok = game_sessions_manager.join_team(session_id, current_user.id, team_id)
    if not ok:
        raise BadRequestError("Команда не найдена или заполнена")
    return game_sessions_manager.get_session_state(session_id)


def leave_team(current_user, session_id: str):
    _require_session(session_id)
    game_sessions_manager.leave_team(session_id, current_user.id)
    return game_sessions_manager.get_session_state(session_id)


def set_ready(current_user, session_id: str):
    _require_session(session_id)
    game_sessions_manager.set_player_ready(session_id, current_user.id)
    return game_sessions_manager.get_session_state(session_id)


def mark_answered(current_user, session_id: str, question_index: int):
    _require_session(session_id)
    game_sessions_manager.mark_answered(session_id, current_user.id, question_index)
    game_sessions_manager.sync_progress(session_id)
    return game_sessions_manager.get_session_state(session_id)


def cast_vote(current_user, session_id: str, question_index: int, answer_ids):
    _require_session(session_id)
    game_sessions_manager.record_vote(session_id, current_user.id, question_index, answer_ids)
    return game_sessions_manager.get_session_state(session_id)


def team_answer(current_user, session_id: str, request):
    _require_session(session_id)
    game_sessions_manager.record_team_answer(
        session_id, current_user.id, request.question_index, request.answer_ids,
        request.points_earned, request.max_possible, request.is_correct,
    )
    game_sessions_manager.sync_progress(session_id)
    return game_sessions_manager.get_session_state(session_id)


def record_result(current_user, session_id: str, request):
    _require_session(session_id)
    game_sessions_manager.record_result(
        session_id, current_user.id, request.score, request.max_score,
        request.correct_count, request.duration_seconds,
    )
    return {"recorded": True}


def get_results(session_id: str):
    results = game_sessions_manager.get_results(session_id)
    if results is None:
        raise NotFoundError("Session not found")
    return results


def start_lobby(current_user, session_id: str):
    _require_session(session_id)
    game_sessions_manager.start_lobby(session_id)
    return game_sessions_manager.get_session_state(session_id)


def get_session_state(current_user, session_id: str):
    _require_session(session_id)
    game_sessions_manager.touch_player(session_id, current_user.id)
    game_sessions_manager.check_disconnects(session_id)
    game_sessions_manager.sync_progress(session_id)
    return game_sessions_manager.get_session_state(session_id)


def submit_answer(db: Session, current_user, request):
    session = _require_session(request.session_id)

    game_sessions_manager.record_answer(
        session_id=request.session_id,
        user_id=current_user.id,
        question_id=request.question_id,
        answer_ids=request.answer_ids,
        is_correct=request.is_correct,
        points_earned=request.points_earned,
    )
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

    all_answered = all(
        request.question_id in player.answers for player in session.players.values()
    )
    time_expired = session.is_time_expired(time_limit_seconds=30)  # TODO: реальное время вопроса
    return {"answer_recorded": True, "can_next_question": all_answered or time_expired}


def next_question(db: Session, current_user, session_id: str):
    _require_session(session_id)
    has_next = game_sessions_manager.next_question(session_id)
    if not has_next:
        game_sessions_manager.end_session(session_id)
        game_crud.end_game_session(db, session_id)
    state = game_sessions_manager.get_session_state(session_id)
    return state, has_next


def finish_game(db: Session, current_user, request):
    session = _require_session(request.session_id)

    game_sessions_manager.end_session(request.session_id)
    game_crud.end_game_session(db, request.session_id)

    quiz = quiz_crud.get_quiz(db, session.quiz_id)
    max_score = sum(q.points for q in quiz.questions) if quiz.questions else 0

    result = game_crud.save_quiz_result(
        db, user_id=current_user.id, quiz_id=session.quiz_id,
        score=request.final_score, max_score=max_score, is_completed=True,
    )
    return {
        "result_id": result.id,
        "score": result.score,
        "max_score": result.max_score,
        "percentage": result.percentage,
    }
