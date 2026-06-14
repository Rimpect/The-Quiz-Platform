"""
Сервис для работы с игровыми сессиями.
Инкапсулирует бизнес-логику и использует CRUD для доступа к данным.
"""
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

from ..crud import crud_game_sessions as game_crud
from ..crud import crud_quiz as quiz_crud
from ..game_services.game_sessions_manager import game_sessions_manager, GameMode


class GameSessionService:
    """Сервис для работы с игровыми сессиями"""

    def __init__(self, db: Session):
        self.db = db

    # ========== СОЗДАНИЕ СЕССИЙ ==========

    def create_game_session(
            self,
            quiz_id: int,
            quiz_title: str,
            total_questions: int,
            game_mode: str,
            user_id: int,
            user_nickname: str,
            team_id: Optional[str] = None,
            team_name: Optional[str] = None
    ) -> Dict:
        """Создание новой игровой сессии"""
        try:
            game_mode_enum = GameMode(game_mode)
        except ValueError:
            raise ValueError("Invalid game mode")

        # Создать сессию в памяти
        session_id = game_sessions_manager.create_session(
            quiz_id=quiz_id,
            quiz_title=quiz_title,
            total_questions=total_questions,
            game_mode=game_mode_enum,
            team_id=team_id,
            team_name=team_name,
        )

        # Сохранить в БД
        game_crud.create_game_session(
            self.db,
            session_id=session_id,
            quiz_id=quiz_id,
            game_mode=game_mode,
            team_id=team_id,
            team_name=team_name,
        )

        # Добавить создателя в сессию
        game_sessions_manager.add_player(
            session_id,
            user_id,
            user_nickname,
        )

        if game_mode == "team":
            game_crud.add_team_member(
                self.db,
                session_id=session_id,
                team_id=team_id,
                user_id=user_id,
            )

        return {"session_id": session_id}

    def create_lobby(
            self,
            quiz_id: int,
            game_mode: str,
            user_id: int,
            user_nickname: str,
            lobby_wait_seconds: Optional[int] = None,
            max_team_members: Optional[int] = None
    ) -> Dict:
        """Создание нового хост-лобби с кодом приглашения"""
        try:
            game_mode_enum = GameMode(game_mode)
        except ValueError:
            raise ValueError("Invalid game mode")

        # Создать join code
        code = game_sessions_manager.generate_join_code()

        # Создать сессию
        session_id = game_sessions_manager.create_session(
            quiz_id=quiz_id,
            quiz_title="",
            total_questions=0,
            game_mode=game_mode_enum,
            lobby_wait_seconds=lobby_wait_seconds or 30,
            max_team_members=max_team_members or 10,
            join_code=code,
        )

        # Назначаем создателя хостом
        session = game_sessions_manager.get_session(session_id)
        if session:
            session.host_id = user_id

        # Добавить игрока
        game_sessions_manager.add_player(
            session_id,
            user_id,
            user_nickname,
        )

        return {
            "session_id": session_id,
            "join_code": code,
        }

    def find_open_lobby(self, quiz_id: int, game_mode: str) -> Optional[str]:
        """Найти открытое лобби для квиза"""
        try:
            game_mode_enum = GameMode(game_mode)
        except ValueError:
            return None

        return game_sessions_manager.find_open_lobby(quiz_id, game_mode_enum)

    # ========== ПРИСОЕДИНЕНИЕ ==========

    def join_game_session(self, session_id: str, user_id: int, user_nickname: str, photo_profile: str = "") -> Dict:
        """Присоединиться к игровой сессии"""
        session = game_sessions_manager.get_session(session_id)
        if not session:
            raise ValueError("Session not found")

        if session.is_finished():
            raise ValueError("Game session is finished")

        # Добавить игрока
        game_sessions_manager.add_player(
            session_id,
            user_id,
            user_nickname,
            photo_profile,
        )

        state = game_sessions_manager.get_session_state(session_id)
        return state

    def join_lobby_by_code(self, code: str, user_id: int, user_nickname: str, photo_profile: str = "") -> Dict:
        """Войти в лобби по коду приглашения"""
        session_id = game_sessions_manager.find_by_code(code)
        if not session_id:
            raise ValueError("Лобби с таким кодом не найдено или уже началось")

        game_sessions_manager.add_player(
            session_id,
            user_id,
            user_nickname,
            photo_profile,
        )

        state = game_sessions_manager.get_session_state(session_id)
        return state

    # ========== УПРАВЛЕНИЕ СЕССИЕЙ ==========

    def leave_session(self, session_id: str, user_id: int) -> Dict:
        """Покинуть лобби"""
        session = game_sessions_manager.get_session(session_id)
        if not session:
            raise ValueError("Session not found")

        cancelled = game_sessions_manager.leave_lobby(session_id, user_id)
        return {"cancelled": cancelled}

    def set_player_ready(self, session_id: str, user_id: int) -> Dict:
        """Отметить игрока готовым"""
        session = game_sessions_manager.get_session(session_id)
        if not session:
            raise ValueError("Session not found")

        game_sessions_manager.set_player_ready(session_id, user_id)
        state = game_sessions_manager.get_session_state(session_id)
        return state

    def start_lobby(self, session_id: str) -> Dict:
        """Старт лобби"""
        session = game_sessions_manager.get_session(session_id)
        if not session:
            raise ValueError("Session not found")

        game_sessions_manager.start_lobby(session_id)
        state = game_sessions_manager.get_session_state(session_id)
        return state

    # ========== КОМАНДЫ ==========

    def create_team(self, session_id: str, user_id: int, team_name: str) -> Dict:
        """Создать команду в лобби"""
        session = game_sessions_manager.get_session(session_id)
        if not session:
            raise ValueError("Session not found")

        team_id = game_sessions_manager.create_team(session_id, user_id, team_name)
        state = game_sessions_manager.get_session_state(session_id)
        return {"team_id": team_id, "state": state}

    def join_team(self, session_id: str, user_id: int, team_id: str) -> Dict:
        """Присоединиться к команде"""
        session = game_sessions_manager.get_session(session_id)
        if not session:
            raise ValueError("Session not found")

        ok = game_sessions_manager.join_team(session_id, user_id, team_id)
        if not ok:
            raise ValueError("Команда не найдена или заполнена")

        state = game_sessions_manager.get_session_state(session_id)
        return state

    def leave_team(self, session_id: str, user_id: int) -> Dict:
        """Покинуть команду"""
        session = game_sessions_manager.get_session(session_id)
        if not session:
            raise ValueError("Session not found")

        game_sessions_manager.leave_team(session_id, user_id)
        state = game_sessions_manager.get_session_state(session_id)
        return state

    # ========== ОТВЕТЫ ==========

    def record_answer(
            self,
            session_id: str,
            user_id: int,
            question_id: int,
            answer_ids: List[int],
            is_correct: bool,
            points_earned: int
    ) -> Dict:
        """Записать ответ игрока"""
        session = game_sessions_manager.get_session(session_id)
        if not session:
            raise ValueError("Session not found")

        game_sessions_manager.record_answer(
            session_id=session_id,
            user_id=user_id,
            question_id=question_id,
            answer_ids=answer_ids,
            is_correct=is_correct,
            points_earned=points_earned,
        )

        return {"answer_recorded": True}

    def mark_answered(self, session_id: str, user_id: int, question_index: int) -> Dict:
        """Отметить, что игрок ответил на вопрос"""
        session = game_sessions_manager.get_session(session_id)
        if not session:
            raise ValueError("Session not found")

        game_sessions_manager.mark_answered(session_id, user_id, question_index)
        game_sessions_manager.sync_progress(session_id)
        state = game_sessions_manager.get_session_state(session_id)
        return state

    def record_vote(self, session_id: str, user_id: int, question_index: int, answer_ids: List[int]) -> Dict:
        """Записать голос игрока (для командного режима)"""
        session = game_sessions_manager.get_session(session_id)
        if not session:
            raise ValueError("Session not found")

        game_sessions_manager.record_vote(session_id, user_id, question_index, answer_ids)
        state = game_sessions_manager.get_session_state(session_id)
        return state

    def record_team_answer(
            self,
            session_id: str,
            user_id: int,
            question_index: int,
            answer_ids: List[int],
            points_earned: int,
            max_possible: int,
            is_correct: bool
    ) -> Dict:
        """Записать ответ команды (только лидер)"""
        session = game_sessions_manager.get_session(session_id)
        if not session:
            raise ValueError("Session not found")

        game_sessions_manager.record_team_answer(
            session_id,
            user_id,
            question_index,
            answer_ids,
            points_earned,
            max_possible,
            is_correct,
        )
        game_sessions_manager.sync_progress(session_id)
        state = game_sessions_manager.get_session_state(session_id)
        return state

    # ========== РЕЗУЛЬТАТЫ ==========

    def record_result(
            self,
            session_id: str,
            user_id: int,
            score: int,
            max_score: int,
            correct_count: int,
            duration_seconds: int
    ) -> Dict:
        """Зафиксировать финальный результат игрока"""
        session = game_sessions_manager.get_session(session_id)
        if not session:
            raise ValueError("Session not found")

        game_sessions_manager.record_result(
            session_id,
            user_id,
            score,
            max_score,
            correct_count,
            duration_seconds,
        )
        return {"recorded": True}

    def get_session_results(self, session_id: str) -> Optional[List[Dict]]:
        """Получить результаты сессии"""
        results = game_sessions_manager.get_results(session_id)
        return results

    # ========== ПЕРЕКЛЮЧЕНИЕ ВОПРОСОВ ==========

    def next_question(self, session_id: str) -> Dict:
        """Перейти на следующий вопрос"""
        session = game_sessions_manager.get_session(session_id)
        if not session:
            raise ValueError("Session not found")

        has_next = game_sessions_manager.next_question(session_id)

        if not has_next:
            game_sessions_manager.end_session(session_id)
            game_crud.end_game_session(self.db, session_id)

        state = game_sessions_manager.get_session_state(session_id)
        return {"has_next": has_next, "state": state}

    def get_session_state(self, session_id: str, user_id: int) -> Dict:
        """Получить состояние сессии (heartbeat)"""
        session = game_sessions_manager.get_session(session_id)
        if not session:
            raise ValueError("Session not found")

        # Heartbeat
        game_sessions_manager.touch_player(session_id, user_id)
        # Проверка отключений
        game_sessions_manager.check_disconnects(session_id)
        # Синхронизация прогресса
        game_sessions_manager.sync_progress(session_id)

        state = game_sessions_manager.get_session_state(session_id)
        return state

    def ban_player(self, session_id: str, user_id: int) -> Dict:
        """Забанить игрока (анти-чит)"""
        session = game_sessions_manager.get_session(session_id)
        if not session:
            raise ValueError("Session not found")

        game_sessions_manager.ban_player(session_id, user_id)
        return {"banned": True}
