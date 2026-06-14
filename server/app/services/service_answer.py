"""
Сервис для работы с ответами.
Инкапсулирует бизнес-логику и использует CRUD для доступа к данным.
"""
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

from ..crud import crud_answer, crud_question
from ..schemas.schemas_answer import AnswerCreate, AnswerUpdate


class AnswerService:
    """Сервис для работы с ответами"""

    def __init__(self, db: Session):
        self.db = db

    # ========== ПОЛУЧЕНИЕ ДАННЫХ ==========

    def get_answer(self, answer_id: int) -> Optional[Dict]:
        """Получение ответа по ID"""
        answer = crud_answer.get_answer(self.db, answer_id)
        if not answer:
            return None
        return self._answer_to_dict(answer)

    def get_answers_by_question(self, question_id: int) -> List[Dict]:
        """Получение всех ответов для вопроса"""
        answers = crud_answer.get_answers_by_question(self.db, question_id)
        return [self._answer_to_dict(a) for a in answers]

    # ========== СОЗДАНИЕ ОТВЕТОВ ==========

    def create_answer(self, answer_data: AnswerCreate, question_id: int) -> Dict:
        """Создание ответа на вопрос"""
        # Проверяем существование вопроса
        if not crud_question.get_question(self.db, question_id):
            raise ValueError("Вопрос не найден")

        answer_dict = {
            "question_id": question_id,
            "answer_text": answer_data.answer_text,
            "is_correct": answer_data.is_correct,
            "order_number": getattr(answer_data, "order_number", None),
        }

        answer = crud_answer.create_answer_record(self.db, answer_dict)
        return self._answer_to_dict(answer)

    def create_answers_bulk(self, answers_data: List[AnswerCreate], question_id: int) -> List[Dict]:
        """Массовое создание ответов на вопрос"""
        # Проверяем существование вопроса
        if not crud_question.get_question(self.db, question_id):
            raise ValueError("Вопрос не найден")

        answers = []
        for idx, answer_data in enumerate(answers_data):
            answer_dict = {
                "question_id": question_id,
                "answer_text": answer_data.answer_text,
                "is_correct": answer_data.is_correct,
                "order_number": answer_data.order_number or idx,
            }
            answer = crud_answer.create_answer_record(self.db, answer_dict)
            answers.append(self._answer_to_dict(answer))

        return answers

    # ========== ОБНОВЛЕНИЕ ОТВЕТОВ ==========

    def update_answer(self, answer_id: int, answer_update: AnswerUpdate) -> Optional[Dict]:
        """Обновление ответа"""
        answer = crud_answer.update_answer(self.db, answer_id, answer_update)
        return self._answer_to_dict(answer) if answer else None

    # ========== УДАЛЕНИЕ ОТВЕТОВ ==========

    def delete_answer(self, answer_id: int) -> bool:
        """Удаление ответа"""
        return crud_answer.delete_answer(self.db, answer_id)

    # ========== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ==========

    def check_answer_belongs_to_question(self, answer_id: int, question_id: int) -> bool:
        """Проверка, что ответ принадлежит вопросу"""
        answer = crud_answer.get_answer(self.db, answer_id)
        if not answer:
            return False
        return answer.question_id == question_id

    # ========== ПРЕОБРАЗОВАНИЯ ==========

    def _answer_to_dict(self, answer) -> Dict:
        """Преобразование Answer в dict для ответа"""
        return {
            "id": answer.id,
            "question_id": answer.question_id,
            "answer_text": answer.answer_text,
            "is_correct": answer.is_correct,
            "order_number": answer.order_number,
        }
