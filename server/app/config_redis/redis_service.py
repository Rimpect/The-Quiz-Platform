"""
Сервисы для работы с Redis
Управление сессиями, лобби и лидербордами
"""
import json
import uuid
from datetime import datetime
from typing import Optional, List, Dict

from .redis_config import get_redis, RedisKeys, SESSION_TTL, ANSWER_TTL, LOBBY_TTL, LEADERBOARD_TTL


class QuizSessionService:
    """Сервис для управления сессиями прохождения квизов в Redis"""

    def __init__(self):
        self.redis = get_redis()

    def create_session(self, user_id: int, quiz_id: int, total_questions: int) -> str:
        """Создание новой сессии прохождения квиза"""
        session_id = str(uuid.uuid4())

        session_data = {
            "session_id": session_id,
            "user_id": str(user_id),
            "quiz_id": str(quiz_id),
            "total_questions": str(total_questions),
            "current_question": "0",
            "status": "in_progress",
            "started_at": datetime.utcnow().isoformat()
        }

        key = RedisKeys.quiz_session(session_id)
        self.redis.hset(key, mapping=session_data)
        self.redis.expire(key, SESSION_TTL)

        return session_id

    def get_session(self, session_id: str) -> Optional[Dict]:
        """Получение данных сессии"""
        key = RedisKeys.quiz_session(session_id)
        data = self.redis.hgetall(key)
        return data if data else None

    def update_session_status(self, session_id: str, status: str):
        """Обновление статуса сессии"""
        key = RedisKeys.quiz_session(session_id)
        self.redis.hset(key, "status", status)
        if status == "completed":
            self.redis.hset(key, "completed_at", datetime.utcnow().isoformat())

    def save_answer(self, session_id: str, question_id: int, user_id: int, answer_data: Dict) -> bool:
        """Сохранение ответа пользователя в Redis"""
        answer_key = RedisKeys.user_answer(session_id, question_id)
        answer_data.update({
            "session_id": session_id,
            "question_id": str(question_id),
            "user_id": str(user_id),
            "answered_at": datetime.utcnow().isoformat()
        })
        self.redis.hset(answer_key, mapping=answer_data)
        self.redis.expire(answer_key, ANSWER_TTL)

        # Добавляем в список ответов сессии
        answers_key = RedisKeys.session_answers(session_id)
        self.redis.sadd(answers_key, answer_key)
        self.redis.expire(answers_key, ANSWER_TTL)

        return True

    def get_answer(self, session_id: str, question_id: int) -> Optional[Dict]:
        """Получение ответа на конкретный вопрос"""
        answer_key = RedisKeys.user_answer(session_id, question_id)
        data = self.redis.hgetall(answer_key)
        return data if data else None

    def get_all_answers(self, session_id: str) -> List[Dict]:
        """Получение всех ответов сессии"""
        answers_key = RedisKeys.session_answers(session_id)
        answer_keys = self.redis.smembers(answers_key)

        answers = []
        for key in answer_keys:
            answer = self.redis.hgetall(key)
            if answer:
                answers.append(answer)

        return sorted(answers, key=lambda x: int(x.get("question_order", 0)))

    def calculate_score(self, session_id: str) -> Dict:
        """Подсчет результатов сессии"""
        answers = self.get_all_answers(session_id)
        session = self.get_session(session_id)

        total_points = sum(int(a.get("points_earned", 0)) for a in answers)
        correct_answers = sum(1 for a in answers if a.get("is_correct") == "True")

        return {
            "session_id": session_id,
            "user_id": int(session.get("user_id")) if session else None,
            "quiz_id": int(session.get("quiz_id")) if session else None,
            "total_points": total_points,
            "total_questions": len(answers),
            "correct_answers": correct_answers,
            "percentage": (total_points / (len(answers) * 10) * 100) if answers else 0
        }

    def delete_session(self, session_id: str):
        """Удаление сессии и всех связанных ответов"""
        session_key = RedisKeys.quiz_session(session_id)
        self.redis.delete(session_key)

        answers_key = RedisKeys.session_answers(session_id)
        answer_keys = self.redis.smembers(answers_key)
        if answer_keys:
            for answer_key in answer_keys:
                self.redis.delete(answer_key)
        self.redis.delete(answers_key)


class LobbyService:
    """Сервис для управления приватными лобби в Redis"""

    def __init__(self):
        self.redis = get_redis()

    def create_lobby(self,
                     host_user_id: int,
                     quiz_id: int,
                     max_players: int = 4,
                     is_public: bool = False
        ) -> str:
        """Создание нового лобби"""
        lobby_id = str(uuid.uuid4())[:8]

        lobby_data = {
            "lobby_id": lobby_id,
            "host_user_id": str(host_user_id),
            "quiz_id": str(quiz_id),
            "max_players": str(max_players),
            "is_public": "true" if is_public else "false",
            "status": "waiting",
            "created_at": datetime.utcnow().isoformat(),
            "players": json.dumps([host_user_id])
        }

        key = RedisKeys.private_lobby(lobby_id)
        self.redis.hset(key, mapping=lobby_data)
        self.redis.expire(key, LOBBY_TTL)

        if is_public:
            index_key = RedisKeys.public_lobbies_index()
            self.redis.zadd(index_key, {lobby_id: datetime.utcnow().timestamp()})
            self.redis.expire(index_key, LOBBY_TTL)


        # Отмечаем, что пользователь в лобби
        user_lobby_key = RedisKeys.user_lobby(host_user_id)
        self.redis.setex(user_lobby_key, LOBBY_TTL, lobby_id)

        return lobby_id

    def get_public_lobbies(self, limit: int = 20) -> List[Dict]:
        """Получение списка публичных лобби"""
        index_key = RedisKeys.public_lobbies_index()
        lobby_ids = self.redis.zrevrange(index_key, 0, limit - 1)

        lobbies = []
        for lobby_id in lobby_ids :
            key = RedisKeys.public_lobby(lobby_id)
            data = self.redis.hgetall(key)
            if data and data.get("status") == "waiting" :
                data["players"] = json.loads(data.get("players", "[]"))
                lobbies.append(data)

        return lobbies



    def get_lobby(self, lobby_id: str) -> Optional[Dict]:
        """Получение данных лобби"""
        key = RedisKeys.private_lobby(lobby_id)
        data = self.redis.hgetall(key)
        if data:
            data["players"] = json.loads(data.get("players", "[]"))
        return data if data else None

    def join_lobby(self, lobby_id: str, user_id: int) -> bool:
        """Присоединение к лобби"""
        lobby = self.get_lobby(lobby_id)
        if not lobby:
            return False

        players = lobby.get("players", [])
        if len(players) >= int(lobby.get("max_players", 4)):
            return False

        if user_id in players:
            return True

        players.append(user_id)

        key = RedisKeys.private_lobby(lobby_id)
        self.redis.hset(key, "players", json.dumps(players))

        user_lobby_key = RedisKeys.user_lobby(user_id)
        self.redis.setex(user_lobby_key, LOBBY_TTL, lobby_id)

        return True

    def leave_lobby(self, lobby_id: str, user_id: int) -> bool:
        """Выход из лобби"""
        lobby = self.get_lobby(lobby_id)
        if not lobby:
            return False

        players = lobby.get("players", [])
        if user_id not in players:
            return False

        players.remove(user_id)

        if len(players) == 0 or user_id == int(lobby.get("host_user_id")):
            self.delete_lobby(lobby_id)
            return True

        key = RedisKeys.private_lobby(lobby_id)
        self.redis.hset(key, "players", json.dumps(players))

        user_lobby_key = RedisKeys.user_lobby(user_id)
        self.redis.delete(user_lobby_key)

        return True

    def delete_lobby(self, lobby_id: str):
        """Удаление лобби"""
        lobby = self.get_lobby(lobby_id)
        if lobby:
            for player_id in lobby.get("players", []):
                user_lobby_key = RedisKeys.user_lobby(player_id)
                self.redis.delete(user_lobby_key)

        key = RedisKeys.private_lobby(lobby_id)
        self.redis.delete(key)

    def start_game(self, lobby_id: str) -> bool:
        """Начало игры в лобби"""
        key = RedisKeys.private_lobby(lobby_id)
        self.redis.hset(key, "status", "playing")
        self.redis.hset(key, "started_at", datetime.utcnow().isoformat())
        return True

    def get_user_lobby(self, user_id: int) -> Optional[Dict]:
        """Получение лобби, в котором находится пользователь"""
        user_lobby_key = RedisKeys.user_lobby(user_id)
        lobby_id = self.redis.get(user_lobby_key)
        if lobby_id:
            return self.get_lobby(lobby_id)
        return None


class LeaderboardService:
    """Сервис для временных лидербордов в Redis"""

    def __init__(self):
        self.redis = get_redis()

    def update_score(self, quiz_id: int, user_id: int, score: int, nickname: str):
        """Обновление счета в лидерборде"""
        key = RedisKeys.quiz_leaderboard(quiz_id)
        self.redis.zadd(key, {f"{user_id}:{nickname}": score})
        self.redis.expire(key, LEADERBOARD_TTL)

    def get_top_scores(self, quiz_id: int, limit: int = 10) -> List[Dict]:
        """Получение топ результатов"""
        key = RedisKeys.quiz_leaderboard(quiz_id)
        results = self.redis.zrevrange(key, 0, limit - 1, withscores=True)

        leaderboard = []
        for member, score in results:
            parts = member.split(":", 1)
            user_id = int(parts[0])
            nickname = parts[1] if len(parts) > 1 else "Unknown"
            leaderboard.append({
                "user_id": user_id,
                "nickname": nickname,
                "score": int(score)
            })
        return leaderboard


def cleanup_expired_sessions() -> int:
    """Очистка истекших сессий в Redis"""
    redis_client = get_redis()
    deleted = 0

    # Очистка сессий
    pattern = RedisKeys.quiz_session("*")
    keys = redis_client.keys(pattern)
    for key in keys:
        if redis_client.ttl(key) <= 0:
            redis_client.delete(key)
            deleted += 1

    # Очистка ответов
    answers_pattern = RedisKeys.session_answers("*")
    answers_keys = redis_client.keys(answers_pattern)
    for key in answers_keys:
        if redis_client.ttl(key) <= 0:
            redis_client.delete(key)
            deleted += 1

    return deleted
