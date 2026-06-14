"""
Сервис для работы с ответами пользователей.
Инкапсулирует бизнес-логику и использует CRUD для доступа к данным.
"""
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from datetime import datetime

from ..crud.crud_user_answer import user_answer_crud
from ..crud import crud_question, crud_answer
from ..schemas.schemas_user_answer import UserAnswerCreate


class UserAnswerService:
    """Сервис для обработки ответов пользователей"""

    def __init__(self, db: Session):
        self.db = db

    # ========== СОЗДАНИЕ И СОХРАНЕНИЕ ОТВЕТОВ ==========

    def save_answer(
            self,
            session_id: str,
            user_id: int,
            quiz_id: int,
            answer_data: UserAnswerCreate
    ) -> Dict[str, Any]:
        """
        Сохранение ответа пользователя

        Args:
            session_id: ID сессии
            user_id: ID пользователя
            quiz_id: ID квиза
            answer_data: Данные ответа

        Returns:
            Dict с результатом сохранения
        """
        # Проверяем существование вопроса
        question = crud_question.get_question(self.db, answer_data.question_id)
        if not question:
            raise ValueError("Вопрос не найден")

        # Проверяем принадлежность вопроса квизу
        if question.quiz_id != quiz_id:
            raise ValueError("Вопрос не принадлежит указанному квизу")

        # Проверяем правильность ответа
        is_correct, points_earned = self._check_answer(
            answer_data.question_id, answer_data
        )

        # Сохраняем ответ через CRUD
        return user_answer_crud.save_answer(
            session_id=session_id,
            user_id=user_id,
            quiz_id=quiz_id,
            question_id=answer_data.question_id,
            answer_data=answer_data,
            is_correct=is_correct,
            points_earned=points_earned
        )

    # ========== ПОЛУЧЕНИЕ ОТВЕТОВ ==========

    def get_answer(self, session_id: str, question_id: int) -> Optional[Dict]:
        """Получение ответа на конкретный вопрос"""
        return user_answer_crud.get_answer(session_id, question_id)

    def get_all_answers(self, session_id: str) -> List[Dict]:
        """Получение всех ответов сессии"""
        return user_answer_crud.get_all_answers(session_id)

    # ========== ПОДСЧЁТ РЕЗУЛЬТАТОВ ==========

    def calculate_score(self, session_id: str) -> Dict[str, Any]:
        """
        Подсчёт результатов сессии

        Args:
            session_id: ID сессии

        Returns:
            Dict с подсчитанными результатами
        """
        answers = self.get_all_answers(session_id)

        if not answers:
            return {
                "session_id": session_id,
                "total_points": 0,
                "total_questions": 0,
                "correct_answers": 0,
                "percentage": 0.0
            }

        total_points = sum(int(a.get("points_earned", 0)) for a in answers)
        correct_answers = sum(1 for a in answers if a.get("is_correct") == "true")
        total_questions = len(answers)

        return {
            "session_id": session_id,
            "total_points": total_points,
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "percentage": (correct_answers / total_questions * 100) if total_questions > 0 else 0.0
        }

    # ========== УДАЛЕНИЕ ОТВЕТОВ ==========

    def delete_session_answers(self, session_id: str) -> int:
        """Удаление всех ответов сессии"""
        return user_answer_crud.delete_session_answers(session_id)

    # ========== БИЗНЕС-ЛОГИКА ПРОВЕРКИ ОТВЕТОВ ==========

    def _check_answer(self, question_id: int, answer_data: UserAnswerCreate) -> tuple[bool, int]:
        """
        Проверка правильности ответа

        Args:
            question_id: ID вопроса
            answer_data: Данные ответа пользователя

        Returns:
            tuple[bool, int]: (правильность, полученные баллы)
        """
        question = crud_question.get_question(self.db, question_id)
        if not question:
            return False, 0

        # В зависимости от типа вопроса проверяем ответ
        if question.answer_type == "single":
            return self._check_single_answer(question, answer_data)

        elif question.answer_type == "multiple":
            return self._check_multiple_answer(question, answer_data)

        return False, 0

    def _check_single_answer(self, question, answer_data: UserAnswerCreate) -> tuple[bool, int]:
        """Проверка ответа для одиночного выбора"""
        if not answer_data.answer_id:
            return False, 0

        answer = crud_answer.get_answer(self.db, answer_data.answer_id)
        if answer and answer.is_correct and answer.question_id == question.id:
            return True, question.points

        return False, 0

    def _check_multiple_answer(self, question, answer_data: UserAnswerCreate) -> tuple[bool, int]:
        """Проверка ответа для множественного выбора"""
        if not answer_data.answer_ids:
            return False, 0

        # Получаем все правильные ответы
        correct_answers = crud_answer.get_correct_answers(self.db, question.id)
        correct_ids = {str(a.id) for a in correct_answers}
        user_ids = {str(aid) for aid in answer_data.answer_ids}

        if user_ids == correct_ids:
            return True, question.points

        return False, 0
