"""
CRUD операции для временных ответов (Redis)
"""
import json
from typing import Dict, Any

from sqlalchemy.orm import Session

from ..config_redis.redis_config import get_redis, RedisKeys
from ..schemas.schemas_user_answer import *

# Время жизни ответов в Redis (секунды)
ANSWER_TTL = 3600  # 1 час


class UserAnswerService:
    """Сервис для работы с ответами пользователей в Redis"""

    def __init__(self):
        self.redis = get_redis()

    def save_answer(
            self,
            session_id: str,
            user_id: int,
            quiz_id: int,
            question_id: int,
            answer_data: UserAnswerCreate,
            db: Session  # Добавляем параметр db
    ) -> Dict[str, Any]:
        """
        Сохранение ответа пользователя в Redis
        """
        # Проверяем правильность ответа (передаём db)
        is_correct, points_earned = self._check_answer(
            question_id, answer_data, db
        )

        # Формируем данные ответа
        answer_key = RedisKeys.user_answer(session_id, question_id)

        answer_dict = {
            "session_id": session_id,
            "user_id": str(user_id),
            "quiz_id": str(quiz_id),
            "question_id": str(question_id),
            "answer_ids": json.dumps(answer_data.answer_ids) if answer_data.answer_ids else "",
            "answer_id": str(answer_data.answer_id) if answer_data.answer_id else "",
            "is_correct": "true" if is_correct else "false",
            "points_earned": str(points_earned),
            "time_spent_seconds": str(answer_data.time_spent_seconds or 0),
            "question_order": str(answer_data.question_order or 0),
            "answered_at": datetime.utcnow().isoformat()
        }

        # Сохраняем в Redis
        self.redis.hset(answer_key, mapping=answer_dict)
        self.redis.expire(answer_key, ANSWER_TTL)

        # Добавляем в список ответов сессии
        session_answers_key = RedisKeys.session_answers(session_id)
        self.redis.sadd(session_answers_key, answer_key)
        self.redis.expire(session_answers_key, ANSWER_TTL)

        return {
            "saved": True,
            "is_correct": is_correct,
            "points_earned": points_earned
        }

    def _check_answer(
            self,
            question_id: int,
            answer_data: UserAnswerCreate,
            db: Session  # Добавляем сессию БД
    ) -> tuple[bool, int]:
        """
        Проверка правильности ответа

        Args:
            question_id: ID вопроса
            answer_data: Данные ответа пользователя
            db: Сессия БД

        Returns:
            tuple[bool, int]: (правильность, полученные баллы)
        """
        from ..crud import crud_question as question_crud
        from ..crud import crud_answer as answer_crud

        # Получаем вопрос из БД
        question = question_crud.get_question(db, question_id)
        if not question:
            return False, 0

        # В зависимости от типа вопроса проверяем ответ
        if question.answer_type == "single":
            # Одиночный выбор
            if answer_data.answer_id:
                answer = answer_crud.get_answer(db, answer_data.answer_id)
                if answer and answer.is_correct:
                    return True, question.points
            return False, 0

        elif question.answer_type == "multiple":
            # Множественный выбор
            if answer_data.answer_ids:
                # Получаем все правильные ответы
                correct_answers = answer_crud.get_correct_answers(db, question_id)
                correct_ids = {str(a.id) for a in correct_answers}
                user_ids = {str(aid) for aid in answer_data.answer_ids}

                if user_ids == correct_ids:
                    return True, question.points
            return False, 0
        return False, 0

    def get_answer(self, session_id: str, question_id: int) -> Optional[Dict]:
        """Получение ответа на конкретный вопрос"""
        answer_key = RedisKeys.user_answer(session_id, question_id)
        data = self.redis.hgetall(answer_key)
        return data if data else None

    def get_all_answers(self, session_id: str) -> List[Dict]:
        """Получение всех ответов сессии"""
        session_answers_key = RedisKeys.session_answers(session_id)
        answer_keys = self.redis.smembers(session_answers_key)

        answers = []
        for key in answer_keys:
            answer = self.redis.hgetall(key)
            if answer:
                answers.append(answer)

        return sorted(answers, key=lambda x: int(x.get("question_order", 0)))

    def calculate_score(self, session_id: str) -> Dict:
        """Подсчет результатов сессии"""
        answers = self.get_all_answers(session_id)

        total_points = sum(int(a.get("points_earned", 0)) for a in answers)
        correct_answers = sum(1 for a in answers if a.get("is_correct") == "true")

        return {
            "session_id": session_id,
            "total_points": total_points,
            "total_questions": len(answers),
            "correct_answers": correct_answers,
            "percentage": (correct_answers / len(answers) * 100) if answers else 0
        }

    def delete_session_answers(self, session_id: str) -> int:
        """Удаление всех ответов сессии"""
        session_answers_key = RedisKeys.session_answers(session_id)
        answer_keys = self.redis.smembers(session_answers_key)

        deleted = 0
        for key in answer_keys:
            self.redis.delete(key)
            deleted += 1

        self.redis.delete(session_answers_key)
        return deleted


# Создаем экземпляр сервиса
user_answer_service = UserAnswerService()
