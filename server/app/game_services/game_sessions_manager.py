"""
Менеджер игровых сессий (в памяти)
Управляет активными играми, синхронизацией вопросов и игроков
"""
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class GameMode(str, Enum):
    SOLO = "solo"
    COMPETITIVE = "competitive"
    TEAM = "team"


@dataclass
class Player:
    """Игрок в сессии"""
    user_id: int
    nickname: str
    photo_profile: str = ""
    is_ready: bool = False
    team_id: Optional[str] = None  # к какой команде присоединился (для team-режима)
    is_leader: bool = False        # лидер команды (создатель)
    team_joined_at: Optional[datetime] = None  # момент вступления в команду (порядок наследования капитанства)
    score: int = 0
    correct_count: int = 0
    is_banned: bool = False  # забанен анти-читом
    last_seen: datetime = field(default_factory=datetime.utcnow)  # для heartbeat
    answers: Dict[int, dict] = field(default_factory=dict)  # {question_id: {answer_ids, time_spent}}
    answered_indices: set = field(default_factory=set)  # индексы вопросов, на которые игрок ответил
    votes: Dict[int, list] = field(default_factory=dict)  # {question_index: [option_indices]} — голоса (team)
    # Финальный результат прохождения (для таблицы результатов по сессии)
    has_finished: bool = False
    result_score: int = 0
    result_max: int = 0
    result_correct: int = 0
    result_duration: int = 0


@dataclass
class GameSessionMemory:
    """Игровая сессия (в памяти)"""
    session_id: str
    quiz_id: int
    game_mode: GameMode
    quiz_title: str
    total_questions: int

    # Состояние
    current_question_index: int = 0
    question_start_time: Optional[datetime] = None
    players: Dict[int, Player] = field(default_factory=dict)  # {user_id: Player}

    # Лобби: True когда игра стартовала и все переходят к вопросам
    lobby_started: bool = False
    # Время ожидания в лобби (сек) — общий серверный отсчёт от created_at
    lobby_wait_seconds: int = 30
    # Код приглашения (для командных хост-лобби)
    join_code: str = ""
    # Хост лобби и флаг отмены (хост вышел)
    host_id: Optional[int] = None
    cancelled: bool = False

    # Для командных игр
    team_id: Optional[str] = None
    team_name: Optional[str] = None
    # Команды внутри лобби: {team_id: team_name}
    teams: Dict[str, str] = field(default_factory=dict)
    max_team_members: int = 10
    # Счёт команд (источник истины для командных результатов):
    # {team_id: {"score": int, "max": int, "correct": int, "counted": set}}
    team_scores: Dict[str, dict] = field(default_factory=dict)

    # Лимиты времени по каждому вопросу (для общего серверного отсчёта)
    question_time_limits: list = field(default_factory=list)

    # Времена
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

    # Вопрос будет на сервере (не передаём её в памяти, загружаем при необходимости)

    def add_player(self, user_id: int, nickname: str, photo_profile: str = ""):
        """Добавить игрока в сессию"""
        if user_id not in self.players:
            self.players[user_id] = Player(
                user_id=user_id, nickname=nickname, photo_profile=photo_profile
            )

    def get_player(self, user_id: int) -> Optional[Player]:
        """Получить игрока"""
        return self.players.get(user_id)

    def all_players_ready(self) -> bool:
        """Все ли активные игроки нажали 'Готов' (минимум 1 игрок)"""
        active = [p for p in self.players.values() if not p.is_banned]
        if not active:
            return False
        return all(player.is_ready for player in active)

    def all_answered_current(self) -> bool:
        """Все ли ответили на текущий вопрос (ранний переход).
        Командный режим: достаточно ответа всех лидеров команд.
        Остальные режимы: все активные игроки. Забаненные не учитываются."""
        if self.game_mode == GameMode.TEAM:
            leaders = [
                p for p in self.players.values()
                if not p.is_banned and p.is_leader
            ]
            if not leaders:
                return False
            return all(
                self.current_question_index in p.answered_indices
                for p in leaders
            )

        active = [p for p in self.players.values() if not p.is_banned]
        if not active:
            return False
        return all(
            self.current_question_index in p.answered_indices for p in active
        )

    def team_leader_answered(self, team_id: Optional[str]) -> bool:
        """Ответил ли лидер указанной команды на текущий вопрос."""
        if not team_id:
            return False
        for p in self.players.values():
            if p.team_id == team_id and p.is_leader and not p.is_banned:
                return self.current_question_index in p.answered_indices
        return False

    def prune_empty_teams(self):
        """Удалить команды, в которых не осталось игроков."""
        used = {p.team_id for p in self.players.values() if p.team_id}
        self.teams = {
            tid: name for tid, name in self.teams.items() if tid in used
        }

    def lobby_time_left(self) -> int:
        """Сколько секунд осталось до авто-старта лобби (общий отсчёт с сервера)."""
        elapsed = (datetime.utcnow() - self.created_at).total_seconds()
        return max(0, int(self.lobby_wait_seconds - elapsed))

    def start_question(self):
        """Начать новый вопрос"""
        self.question_start_time = datetime.utcnow()

    def is_time_expired(self, time_limit_seconds: int) -> bool:
        """Проверить истекло ли время для вопроса"""
        if not self.question_start_time:
            return False
        elapsed = (datetime.utcnow() - self.question_start_time).total_seconds()
        return elapsed >= time_limit_seconds

    def get_question_elapsed_seconds(self) -> int:
        """Получить прошедшее время для текущего вопроса"""
        if not self.question_start_time:
            return 0
        return int((datetime.utcnow() - self.question_start_time).total_seconds())

    def current_time_limit(self) -> int:
        """Лимит времени для текущего вопроса (сек). Дефолт 30, если не задан."""
        if 0 <= self.current_question_index < len(self.question_time_limits):
            lim = self.question_time_limits[self.current_question_index]
            if lim and lim > 0:
                return lim
        return 30

    def time_left(self) -> int:
        """Сколько секунд осталось на текущий вопрос (общий отсчёт с сервера)."""
        if not self.question_start_time:
            return self.current_time_limit()
        elapsed = (datetime.utcnow() - self.question_start_time).total_seconds()
        return max(0, int(self.current_time_limit() - elapsed))

    def next_question(self) -> bool:
        """Перейти на следующий вопрос. Возвращает True если есть ещё вопросы"""
        if self.current_question_index + 1 < self.total_questions:
            self.current_question_index += 1
            self.start_question()
            return True
        return False

    def is_finished(self) -> bool:
        """Закончилась ли игра"""
        return self.ended_at is not None


class GameSessionsManager:
    """Менеджер всех активных игровых сессий"""

    def __init__(self, session_ttl_minutes: int = 180):
        self.sessions: Dict[str, GameSessionMemory] = {}
        self.session_ttl = timedelta(minutes=session_ttl_minutes)
        # Redis-зеркало командных сессий (импорт здесь — чтобы не было цикла)
        from .game_session_repo import RedisGameStore
        self.store = RedisGameStore()

    def _persist(self, session: Optional[GameSessionMemory]) -> None:
        """Write-through: командные сессии зеркалируем в Redis (если он есть)."""
        if session is not None and session.game_mode == GameMode.TEAM and self.store.enabled:
            self.store.save(session)

    def create_session(
        self,
        quiz_id: int,
        quiz_title: str,
        total_questions: int,
        game_mode: GameMode,
        team_id: Optional[str] = None,
        team_name: Optional[str] = None,
        question_time_limits: Optional[list] = None,
        lobby_wait_seconds: int = 30,
        max_team_members: int = 10,
        join_code: str = "",
    ) -> str:
        """Создать новую игровую сессию"""
        session_id = str(uuid.uuid4())

        session = GameSessionMemory(
            session_id=session_id,
            quiz_id=quiz_id,
            game_mode=game_mode,
            quiz_title=quiz_title,
            total_questions=total_questions,
            team_id=team_id,
            team_name=team_name,
            question_time_limits=question_time_limits or [],
            lobby_wait_seconds=lobby_wait_seconds or 30,
            max_team_members=max_team_members or 10,
            join_code=join_code,
        )

        self.sessions[session_id] = session
        self._persist(session)
        return session_id

    def generate_join_code(self) -> str:
        """Сгенерировать уникальный 6-значный код приглашения."""
        import random
        import string
        alphabet = string.ascii_uppercase + string.digits
        existing = {s.join_code for s in self.sessions.values() if s.join_code}
        for _ in range(50):
            code = "".join(random.choices(alphabet, k=6))
            if code not in existing:
                return code
        return uuid.uuid4().hex[:6].upper()

    def find_by_code(self, code: str) -> Optional[str]:
        """Найти session_id открытого лобби по коду приглашения."""
        if not code:
            return None
        code = code.strip().upper()
        now = datetime.utcnow()
        for sid, session in self.sessions.items():
            if (now - session.created_at) > self.session_ttl:
                continue
            if (
                session.join_code == code
                and not session.lobby_started
                and not session.is_finished()
                and not session.cancelled
            ):
                return sid

        # Не нашли в памяти — пробуем Redis (после рестарта/другого процесса)
        if self.store.enabled:
            sid = self.store.find_by_code(code)
            if sid:
                session = self.get_session(sid)  # гидратирует в память
                if (
                    session
                    and not session.lobby_started
                    and not session.is_finished()
                    and not session.cancelled
                ):
                    return sid
        return None

    def leave_lobby(self, session_id: str, user_id: int) -> bool:
        """Игрок покидает лобби. Если вышел ХОСТ и игра ещё не началась —
        лобби отменяется для всех. Возвращает True, если лобби отменено."""
        session = self.get_session(session_id)
        if not session:
            return False

        is_host = session.host_id is not None and user_id == session.host_id
        # Отмена только в фазе лобби: во время квиза выход хоста ничего не ломает
        if is_host and not session.lobby_started:
            session.cancelled = True
            return True

        # Обычный игрок — убираем из сессии и чистим пустые команды
        if user_id in session.players:
            del session.players[user_id]
            session.prune_empty_teams()
        return False

    def touch_player(self, session_id: str, user_id: int) -> None:
        """Heartbeat: отметить, что игрок на связи (на каждом опросе)."""
        session = self.get_session(session_id)
        if not session:
            return
        player = session.get_player(user_id)
        if player:
            player.last_seen = datetime.utcnow()

    def ban_player(self, session_id: str, user_id: int) -> None:
        """Забанить игрока анти-читом (только его, остальные продолжают).
        В командном режиме при бане лидера капитанство переходит к самому
        раннему по вступлению незабаненному участнику; если забанена вся
        команда — она снимается с участия."""
        session = self.get_session(session_id)
        if not session:
            return
        player = session.get_player(user_id)
        if not player:
            return

        player.is_banned = True
        if session.game_mode == GameMode.TEAM and player.team_id:
            player.is_leader = False  # забаненный не может быть капитаном
            self._ensure_team_leader(session, player.team_id)

    def _ensure_team_leader(self, session: "GameSessionMemory", team_id: str) -> None:
        """Гарантировать активного капитана у команды.
        Нет незабаненных участников → команда снимается с участия."""
        members = [
            p for p in session.players.values()
            if p.team_id == team_id and not p.is_banned
        ]
        if not members:
            # Вся команда забанена — убираем из лобби и результатов
            session.teams.pop(team_id, None)
            session.team_scores.pop(team_id, None)
            return
        if any(p.is_leader for p in members):
            return
        # Капитанство — самому раннему по вступлению в команду
        from datetime import datetime as _dt
        members.sort(
            key=lambda p: (p.team_joined_at or _dt.max, p.user_id)
        )
        members[0].is_leader = True

    def check_disconnects(self, session_id: str, timeout_seconds: int = 12) -> None:
        """Отвал по таймауту heartbeat. В фазе ЛОББИ: хост отвалился → отмена,
        обычный игрок → убираем. Во время квиза не трогаем (идёт по таймеру)."""
        session = self.get_session(session_id)
        if not session or session.lobby_started or session.cancelled:
            return
        now = datetime.utcnow()
        dead = [
            uid for uid, p in session.players.items()
            if (now - p.last_seen).total_seconds() > timeout_seconds
        ]
        for uid in dead:
            if session.host_id is not None and uid == session.host_id:
                session.cancelled = True
                return
            del session.players[uid]
        if dead:
            session.prune_empty_teams()

    def sync_progress(self, session_id: str) -> None:
        """Двигает общий прогресс при опросе состояния:
        1) авто-старт лобби, когда истёк общий таймер ожидания;
        2) авто-переход на следующий вопрос, когда истекло время текущего.
        Так таймеры и переходы одинаковы для всех игроков."""
        session = self.get_session(session_id)
        if not session or session.is_finished():
            return

        # 1) Авто-старт лобби по общему таймеру
        if not session.lobby_started:
            if session.lobby_time_left() <= 0:
                self.start_lobby(session_id)
            return

        # 2) Авто-переход между вопросами: по таймеру ИЛИ когда все ответили
        if not session.question_start_time:
            return
        elapsed = (datetime.utcnow() - session.question_start_time).total_seconds()
        time_expired = elapsed >= session.current_time_limit()
        if time_expired or session.all_answered_current():
            has_next = session.next_question()  # сбрасывает таймер на текущий момент
            if not has_next:
                session.ended_at = datetime.utcnow()

    def mark_answered(self, session_id: str, user_id: int, question_index: int) -> bool:
        """Отметить, что игрок ответил на вопрос (для раннего перехода)."""
        session = self.get_session(session_id)
        if not session:
            return False
        player = session.get_player(user_id)
        if player:
            player.answered_indices.add(question_index)
        return True

    def record_vote(
        self, session_id: str, user_id: int,
        question_index: int, answer_ids: list,
    ) -> bool:
        """Голос игрока за варианты текущего вопроса (команда видит аватары).
        Перезапись = смена голоса (разрешена, пока лидер не зафиксировал ответ)."""
        session = self.get_session(session_id)
        if not session:
            return False
        player = session.get_player(user_id)
        if not player:
            return False
        # Нельзя менять голос после ответа лидера команды
        if session.team_leader_answered(player.team_id):
            return False
        player.votes[question_index] = list(answer_ids or [])
        return True

    def record_team_answer(
        self, session_id: str, user_id: int, question_index: int,
        answer_ids: list, points: int, max_possible: int, is_correct: bool,
    ) -> bool:
        """Финальный ответ команды (только лидер): фиксируем голос лидера,
        отмечаем его ответившим и копим командный счёт (идемпотентно)."""
        session = self.get_session(session_id)
        if not session:
            return False
        player = session.get_player(user_id)
        if not player or not player.is_leader or not player.team_id:
            return False

        # Голос лидера — чтобы его аватар тоже отображался на вариантах
        player.votes[question_index] = list(answer_ids or [])
        player.answered_indices.add(question_index)

        agg = session.team_scores.setdefault(
            player.team_id,
            {"score": 0, "max": 0, "correct": 0, "counted": set()},
        )
        # Guard: один вопрос засчитывается команде один раз
        if question_index not in agg["counted"]:
            agg["counted"].add(question_index)
            agg["score"] += int(points or 0)
            if is_correct:
                agg["correct"] += 1
        agg["max"] = max(agg["max"], int(max_possible or 0))
        return True

    def record_result(
        self,
        session_id: str,
        user_id: int,
        score: int,
        max_score: int,
        correct: int,
        duration: int,
    ) -> bool:
        """Зафиксировать финальный результат игрока в сессии."""
        session = self.get_session(session_id)
        if not session:
            return False
        player = session.get_player(user_id)
        if player:
            player.has_finished = True
            player.result_score = score
            player.result_max = max_score
            player.result_correct = correct
            player.result_duration = duration
        self._persist(session)
        return True

    def get_results(self, session_id: str) -> Optional[list]:
        """Таблица результатов по сессии (только те, кто играл вместе сейчас).
        Командный режим — агрегат по командам, остальные — по игрокам."""
        session = self.get_session(session_id)
        if not session:
            return None

        finished = [
            p for p in session.players.values()
            if p.has_finished and not p.is_banned
        ]

        # ---- Командный режим: одна строка на команду ----
        # Источник истины — team_scores (ответ команды = ответ капитана),
        # суммировать по участникам нельзя: счёт у всех одинаков и умножился бы.
        if session.game_mode == GameMode.TEAM:
            # Показываем все команды, которые участвовали (есть завершившие
            # игроки), даже если они не набрали очков — иначе при «никто не
            # ответил» таблица была бы пустой.
            team_ids = {p.team_id for p in finished if p.team_id}
            team_ids |= set(session.team_scores.keys())

            rows = []
            for tid in team_ids:
                agg = session.team_scores.get(tid, {})
                members = sum(
                    1 for p in session.players.values()
                    if p.team_id == tid and not p.is_banned
                )
                if members == 0:
                    continue
                # Длительность — по лидеру команды (если он записал результат)
                duration = 0
                for p in session.players.values():
                    if p.team_id == tid and p.is_leader and p.has_finished:
                        duration = p.result_duration
                        break
                rows.append({
                    "name": session.teams.get(tid, "Команда"),
                    "score": agg.get("score", 0),
                    "max": agg.get("max", 0),
                    "correct": agg.get("correct", 0),
                    "members": members,
                    "duration": duration,
                })

            # Сортировка: больше очков, при равенстве — меньше время
            rows.sort(key=lambda t: (-t["score"], t["duration"]))

            results = []
            for idx, t in enumerate(rows, 1):
                percent = int(round(t["score"] / t["max"] * 100)) if t["max"] else 0
                dur = t["duration"]
                results.append({
                    "place": idx,
                    "name": t["name"],
                    "avatar": "",          # у команд нет иконки
                    "is_team": True,
                    "score": t["score"],
                    "max_score": t["max"],
                    "percent": percent,
                    "correct": t["correct"],
                    "members": t["members"],
                    "time": f"{dur // 60}:{dur % 60:02d}",
                })
            return results

        # ---- По игрокам ----
        finished.sort(key=lambda p: (-p.result_score, p.result_duration))
        results = []
        for idx, p in enumerate(finished, 1):
            percent = (
                int(round(p.result_score / p.result_max * 100))
                if p.result_max > 0 else 0
            )
            mins = p.result_duration // 60
            secs = p.result_duration % 60
            results.append({
                "place": idx,
                "user_id": p.user_id,
                "name": p.nickname or "Игрок",
                "avatar": p.photo_profile or "",
                "is_team": False,
                "score": p.result_score,
                "max_score": p.result_max,
                "percent": percent,
                "correct": p.result_correct,
                "time": f"{mins}:{secs:02d}",
                "team_name": session.teams.get(p.team_id) if p.team_id else None,
            })
        return results

    def get_session(self, session_id: str) -> Optional[GameSessionMemory]:
        """Получить сессию"""
        session = self.sessions.get(session_id)

        # Промах в памяти — пробуем восстановить командную сессию из Redis
        # (например, после рестарта сервера).
        if session is None and self.store.enabled:
            restored = self.store.load(session_id)
            if restored is not None:
                self.sessions[session_id] = restored
                session = restored

        # Проверить TTL
        if session and (datetime.utcnow() - session.created_at) > self.session_ttl:
            del self.sessions[session_id]
            return None

        return session

    def find_open_lobby(self, quiz_id: int, game_mode: GameMode) -> Optional[str]:
        """Найти открытое лобби для квиза (ещё не стартовало и не завершено)"""
        now = datetime.utcnow()
        for sid, session in self.sessions.items():
            if (now - session.created_at) > self.session_ttl:
                continue
            if (
                session.quiz_id == quiz_id
                and session.game_mode == game_mode
                and not session.lobby_started
                and not session.is_finished()
                and not session.cancelled
            ):
                return sid
        return None

    def add_player(self, session_id: str, user_id: int, nickname: str, photo_profile: str = "") -> bool:
        """Добавить игрока в сессию"""
        session = self.get_session(session_id)
        if not session:
            return False

        session.add_player(user_id, nickname, photo_profile)
        if not session.started_at:
            session.started_at = datetime.utcnow()
        if not session.question_start_time:
            session.start_question()

        return True

    def set_player_ready(self, session_id: str, user_id: int) -> bool:
        """Отметить игрока готовым. Возвращает True если игра стартовала (все готовы)"""
        session = self.get_session(session_id)
        if not session:
            return False

        player = session.get_player(user_id)
        if player:
            player.is_ready = True

        # Если все готовы — стартуем лобби
        if session.all_players_ready():
            self.start_lobby(session_id)

        return session.lobby_started

    def start_lobby(self, session_id: str) -> bool:
        """Стартовать игру из лобби (по готовности всех или по истечении таймера)"""
        session = self.get_session(session_id)
        if not session:
            return False

        if not session.lobby_started:
            session.lobby_started = True
            session.current_question_index = 0
            session.start_question()

        return True

    def create_team(self, session_id: str, user_id: int, team_name: str) -> Optional[str]:
        """Создать команду в лобби и назначить игрока её лидером"""
        session = self.get_session(session_id)
        if not session:
            return None

        team_id = f"team-{uuid.uuid4().hex[:8]}"
        session.teams[team_id] = team_name

        player = session.get_player(user_id)
        if player:
            player.team_id = team_id
            player.is_leader = True
            player.is_ready = False
            player.team_joined_at = datetime.utcnow()

        session.prune_empty_teams()  # старая команда игрока могла опустеть
        return team_id

    def join_team(self, session_id: str, user_id: int, team_id: str) -> bool:
        """Присоединить игрока к существующей команде (с учётом лимита)"""
        session = self.get_session(session_id)
        if not session or team_id not in session.teams:
            return False

        # Проверка лимита участников (не считая самого игрока, если он уже там)
        members = [
            p for p in session.players.values()
            if p.team_id == team_id and p.user_id != user_id
        ]
        if len(members) >= session.max_team_members:
            return False

        player = session.get_player(user_id)
        if player:
            player.team_id = team_id
            player.is_leader = False
            player.is_ready = False
            player.team_joined_at = datetime.utcnow()

        session.prune_empty_teams()  # старая команда игрока могла опустеть
        return True

    def leave_team(self, session_id: str, user_id: int) -> bool:
        """Игрок покидает свою команду"""
        session = self.get_session(session_id)
        if not session:
            return False

        player = session.get_player(user_id)
        if player:
            player.team_id = None
            player.is_leader = False
            player.is_ready = False

        session.prune_empty_teams()  # команда могла остаться без игроков
        return True

    def record_answer(
        self,
        session_id: str,
        user_id: int,
        question_id: int,
        answer_ids: List[int],
        is_correct: bool,
        points_earned: int,
    ) -> bool:
        """Записать ответ игрока"""
        session = self.get_session(session_id)
        if not session:
            return False

        player = session.get_player(user_id)
        if not player:
            return False

        time_spent = session.get_question_elapsed_seconds()

        player.answers[question_id] = {
            'answer_ids': answer_ids,
            'is_correct': is_correct,
            'points_earned': points_earned,
            'time_spent_seconds': time_spent,
        }

        if is_correct:
            player.correct_count += 1
        player.score += points_earned

        return True

    def next_question(self, session_id: str) -> bool:
        """Перейти на следующий вопрос для всех игроков"""
        session = self.get_session(session_id)
        if not session:
            return False

        has_next = session.next_question()

        if not has_next:
            session.ended_at = datetime.utcnow()

        return has_next

    def end_session(self, session_id: str) -> bool:
        """Завершить сессию"""
        session = self.get_session(session_id)
        if not session:
            return False

        session.ended_at = datetime.utcnow()
        self._persist(session)
        return True

    def get_session_state(self, session_id: str) -> Optional[dict]:
        """Получить состояние сессии для отправки клиентам"""
        session = self.get_session(session_id)
        if not session:
            return None

        # Write-through: командные сессии зеркалируем в Redis. Этот метод
        # вызывается в конце каждого эндпоинта, поэтому покрывает все изменения.
        self._persist(session)

        # Сгруппировать игроков по командам (для team-режима)
        teams = []
        for team_id, team_name in session.teams.items():
            members = [
                {
                    'user_id': p.user_id,
                    'nickname': p.nickname,
                    'photo_profile': p.photo_profile,
                    'is_ready': p.is_ready,
                    'is_leader': p.is_leader,
                }
                for p in session.players.values()
                if p.team_id == team_id
            ]
            agg = session.team_scores.get(team_id) or {}
            teams.append({
                'id': team_id,
                'name': team_name,
                'max_members': session.max_team_members,
                'members': members,
                'score': agg.get('score', 0),
                'correct': agg.get('correct', 0),
                'leader_answered': session.team_leader_answered(team_id),
            })

        # Голоса по текущему вопросу (для оверлея аватаров в команде)
        idx = session.current_question_index
        current_votes = [
            {
                'user_id': p.user_id,
                'nickname': p.nickname,
                'photo_profile': p.photo_profile,
                'team_id': p.team_id,
                'answer_ids': p.votes.get(idx, []),
            }
            for p in session.players.values()
            if p.votes.get(idx)
        ]

        return {
            'session_id': session.session_id,
            'quiz_id': session.quiz_id,
            'game_mode': session.game_mode.value,
            'current_question_index': session.current_question_index,
            'total_questions': session.total_questions,
            'time_left': session.time_left(),
            'question_time_limit': session.current_time_limit(),
            'team_id': session.team_id,
            'team_name': session.team_name,
            'is_finished': session.is_finished(),
            'lobby_started': session.lobby_started,
            'lobby_time_left': session.lobby_time_left(),
            'join_code': session.join_code,
            'cancelled': session.cancelled,
            'host_id': session.host_id,
            'teams': teams,
            'current_votes': current_votes,
            'players': [
                {
                    'user_id': player.user_id,
                    'nickname': player.nickname,
                    'photo_profile': player.photo_profile,
                    'is_ready': player.is_ready,
                    'team_id': player.team_id,
                    'is_leader': player.is_leader,
                    'is_banned': player.is_banned,
                    'score': player.score,
                    'correct_count': player.correct_count,
                    # ответил/проголосовал на текущем вопросе
                    'answered_current': (
                        idx in player.answered_indices
                        or bool(player.votes.get(idx))
                    ),
                    # на связи (heartbeat за последние 10 сек)
                    'online': (
                        (datetime.utcnow() - player.last_seen).total_seconds()
                        <= 10
                    ),
                }
                for player in session.players.values()
            ],
        }

    def cleanup_expired_sessions(self):
        """Удалить истекшие сессии"""
        now = datetime.utcnow()
        expired = [
            sid for sid, session in self.sessions.items()
            if (now - session.created_at) > self.session_ttl
        ]
        for sid in expired:
            del self.sessions[sid]


# Глобальный экземпляр менеджера
game_sessions_manager = GameSessionsManager()
