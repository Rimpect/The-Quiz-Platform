"""
Redis-хранилище командных игровых сессий.

Фаза 1: write-through зеркалирование. Рабочая копия живёт в памяти
(GameSessionsManager), а сюда сессия сохраняется при каждом изменении и
загружается обратно, если её нет в памяти (переживание рестарта сервера).
Если Redis недоступен — все методы безопасные no-op (None), менеджер
продолжает работать чисто в памяти.
"""
from datetime import datetime
from typing import Optional

from ..config_redis.redis_config import get_redis, RedisKeys
# Классы определены выше создания глобального экземпляра менеджера,
# поэтому импорт на уровне модуля безопасен (без цикла).
from .game_sessions_manager import GameMode, Player, GameSessionMemory

SESSION_TTL_SECONDS = 180 * 60  # как session_ttl менеджера (180 минут)


def _dt(value: Optional[datetime]) -> Optional[str]:
    return value.isoformat() if value else None


def _parse_dt(value: Optional[str]) -> Optional[datetime]:
    return datetime.fromisoformat(value) if value else None


def _player_to_dict(p: Player) -> dict:
    return {
        "user_id": p.user_id,
        "nickname": p.nickname,
        "photo_profile": p.photo_profile,
        "is_ready": p.is_ready,
        "team_id": p.team_id,
        "is_leader": p.is_leader,
        "team_joined_at": _dt(p.team_joined_at),
        "score": p.score,
        "correct_count": p.correct_count,
        "is_banned": p.is_banned,
        "last_seen": _dt(p.last_seen),
        # ключи-словарей в JSON становятся строками — на загрузке приводим обратно к int
        "answers": {str(k): v for k, v in p.answers.items()},
        "answered_indices": list(p.answered_indices),
        "votes": {str(k): v for k, v in p.votes.items()},
        "has_finished": p.has_finished,
        "result_score": p.result_score,
        "result_max": p.result_max,
        "result_correct": p.result_correct,
        "result_duration": p.result_duration,
    }


def _player_from_dict(d: dict) -> Player:
    p = Player(
        user_id=d["user_id"],
        nickname=d.get("nickname", ""),
        photo_profile=d.get("photo_profile", ""),
    )
    p.is_ready = d.get("is_ready", False)
    p.team_id = d.get("team_id")
    p.is_leader = d.get("is_leader", False)
    p.team_joined_at = _parse_dt(d.get("team_joined_at"))
    p.score = d.get("score", 0)
    p.correct_count = d.get("correct_count", 0)
    p.is_banned = d.get("is_banned", False)
    p.last_seen = _parse_dt(d.get("last_seen")) or datetime.utcnow()
    p.answers = {int(k): v for k, v in (d.get("answers") or {}).items()}
    p.answered_indices = set(d.get("answered_indices") or [])
    p.votes = {int(k): v for k, v in (d.get("votes") or {}).items()}
    p.has_finished = d.get("has_finished", False)
    p.result_score = d.get("result_score", 0)
    p.result_max = d.get("result_max", 0)
    p.result_correct = d.get("result_correct", 0)
    p.result_duration = d.get("result_duration", 0)
    return p


def session_to_dict(s: GameSessionMemory) -> dict:
    return {
        "session_id": s.session_id,
        "quiz_id": s.quiz_id,
        "game_mode": s.game_mode.value,
        "quiz_title": s.quiz_title,
        "total_questions": s.total_questions,
        "current_question_index": s.current_question_index,
        "question_start_time": _dt(s.question_start_time),
        "players": {str(uid): _player_to_dict(p) for uid, p in s.players.items()},
        "lobby_started": s.lobby_started,
        "lobby_wait_seconds": s.lobby_wait_seconds,
        "join_code": s.join_code,
        "host_id": s.host_id,
        "cancelled": s.cancelled,
        "team_id": s.team_id,
        "team_name": s.team_name,
        "teams": s.teams,
        "max_team_members": s.max_team_members,
        "team_scores": {
            tid: {
                "score": agg.get("score", 0),
                "max": agg.get("max", 0),
                "correct": agg.get("correct", 0),
                "counted": list(agg.get("counted", set())),
            }
            for tid, agg in s.team_scores.items()
        },
        "question_time_limits": s.question_time_limits,
        "created_at": _dt(s.created_at),
        "started_at": _dt(s.started_at),
        "ended_at": _dt(s.ended_at),
    }


def session_from_dict(d: dict) -> GameSessionMemory:
    s = GameSessionMemory(
        session_id=d["session_id"],
        quiz_id=d["quiz_id"],
        game_mode=GameMode(d["game_mode"]),
        quiz_title=d.get("quiz_title", ""),
        total_questions=d.get("total_questions", 0),
    )
    s.current_question_index = d.get("current_question_index", 0)
    s.question_start_time = _parse_dt(d.get("question_start_time"))
    s.players = {
        int(uid): _player_from_dict(pd) for uid, pd in (d.get("players") or {}).items()
    }
    s.lobby_started = d.get("lobby_started", False)
    s.lobby_wait_seconds = d.get("lobby_wait_seconds", 30)
    s.join_code = d.get("join_code", "")
    s.host_id = d.get("host_id")
    s.cancelled = d.get("cancelled", False)
    s.team_id = d.get("team_id")
    s.team_name = d.get("team_name")
    s.teams = d.get("teams") or {}
    s.max_team_members = d.get("max_team_members", 10)
    s.team_scores = {
        tid: {
            "score": agg.get("score", 0),
            "max": agg.get("max", 0),
            "correct": agg.get("correct", 0),
            "counted": set(agg.get("counted") or []),
        }
        for tid, agg in (d.get("team_scores") or {}).items()
    }
    s.question_time_limits = d.get("question_time_limits") or []
    s.created_at = _parse_dt(d.get("created_at")) or datetime.utcnow()
    s.started_at = _parse_dt(d.get("started_at"))
    s.ended_at = _parse_dt(d.get("ended_at"))
    return s


class RedisGameStore:
    """Зеркало командных сессий в Redis.

    Отказоустойчиво: если Redis недоступен (не установлен, не настроен или
    сервер не запущен) — все операции тихо деградируют, игра идёт в памяти.
    Простой circuit breaker: после сбоя соединения отключаемся на COOLDOWN сек,
    чтобы не дёргать недоступный Redis на каждом запросе.
    """

    COOLDOWN_SECONDS = 30

    def __init__(self):
        self._redis = get_redis()
        self._disabled_until = 0.0  # время (monotonic), до которого Redis считаем недоступным

    @property
    def enabled(self) -> bool:
        if self._redis is None:
            return False
        import time
        return time.monotonic() >= self._disabled_until

    def _trip(self) -> None:
        """Открыть «предохранитель» после сбоя соединения."""
        import time
        self._disabled_until = time.monotonic() + self.COOLDOWN_SECONDS

    def save(self, session: GameSessionMemory) -> None:
        if not self.enabled:
            return
        import json
        try:
            data = json.dumps(session_to_dict(session))
            self._redis.set(
                RedisKeys.game_session(session.session_id), data, ex=SESSION_TTL_SECONDS
            )
            if session.join_code and not session.lobby_started:
                self._redis.set(
                    RedisKeys.game_code(session.join_code),
                    session.session_id,
                    ex=SESSION_TTL_SECONDS,
                )
        except Exception:
            self._trip()

    def load(self, session_id: str) -> Optional[GameSessionMemory]:
        if not self.enabled:
            return None
        import json
        try:
            raw = self._redis.get(RedisKeys.game_session(session_id))
        except Exception:
            self._trip()
            return None
        if not raw:
            return None
        try:
            return session_from_dict(json.loads(raw))
        except (ValueError, KeyError):
            return None

    def find_by_code(self, code: str) -> Optional[str]:
        if not self.enabled or not code:
            return None
        try:
            return self._redis.get(RedisKeys.game_code(code))
        except Exception:
            self._trip()
            return None

    def delete(self, session_id: str) -> None:
        if not self.enabled:
            return
        try:
            self._redis.delete(RedisKeys.game_session(session_id))
        except Exception:
            self._trip()
