"""
Сервис для работы с вопросами.
Инкапсулирует бизнес-логику и использует CRUD для доступа к данным.
"""
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

from ..crud import crud_question, crud_quiz
from ..schemas.schemas_question import QuestionCreate, QuestionUpdate


class QuestionService:
    """Сервис для работы с вопросами"""

    def __init__(self, db: Session):
        self.db = db

    # ========== ПОЛУЧЕНИЕ ДАННЫХ ==========

    def get_question(self, question_id: int) -> Optional[Dict]:
        """Получение вопроса по ID"""
        question = crud_question.get_question(self.db, question_id)
        if not question:
            return None
        return self._question_to_dict(question)

    def get_questions_by_quiz(self, quiz_id: int, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Получение всех вопросов квиза"""
        questions = crud_question.get_questions_by_quiz(self.db, quiz_id, skip, limit)
        return [self._question_to_dict(q) for q in questions]

    # ========== СОЗДАНИЕ ВОПРОСОВ ==========

    def create_question(self, question_data: QuestionCreate, quiz_id: int) -> Dict:
        """Создание вопроса в квизе"""
        # Проверяем существование квиза
        if not crud_quiz.get_quiz(self.db, quiz_id):
            raise ValueError("Квиз не найден")

        question_dict = {
            "quiz_id": quiz_id,
            "answer_type": question_data.answer_type,
            "points": question_data.points,
            "question_text": question_data.question_text,
            "question_media_url": getattr(question_data, "question_media_url", None),
            "time_limit_seconds": question_data.time_limit_seconds,
        }

        question = crud_question.create_question_record(self.db, question_dict)
        return self._question_to_dict(question)

    # ========== ОБНОВЛЕНИЕ ВОПРОСОВ ==========

    def update_question(self, question_id: int, question_update: QuestionUpdate) -> Optional[Dict]:
        """Обновление вопроса"""
        question = crud_question.update_question(self.db, question_id, question_update)
        return self._question_to_dict(question) if question else None

    # ========== УДАЛЕНИЕ ВОПРОСОВ ==========

    def delete_question(self, question_id: int) -> bool:
        """Удаление вопроса"""
        return crud_question.delete_question(self.db, question_id)

    # ========== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ==========

    def check_question_belongs_to_quiz(self, question_id: int, quiz_id: int) -> bool:
        """Проверка, что вопрос принадлежит квизу"""
        question = crud_question.get_question(self.db, question_id)
        if not question:
            return False
        return question.quiz_id == quiz_id

    # ========== ПРЕОБРАЗОВАНИЯ ==========

    def _question_to_dict(self, question) -> Dict:
        """Преобразование Question в dict для ответа"""
        return {
            "id": question.id,
            "quiz_id": question.quiz_id,
            "answer_type": question.answer_type,
            "points": question.points,
            "question_text": question.question_text,
            "question_media_url": getattr(question, "question_media_url", None),
            "time_limit_seconds": question.time_limit_seconds,
            "answers": [
                {
                    "id": a.id,
                    "answer_text": a.answer_text,
                    "is_correct": a.is_correct,
                    "order_number": a.order_number,
                }
                for a in question.answers
            ] if hasattr(question, 'answers') else [],
        }
