"""
Сервис для работы с результатами квизов.
Инкапсулирует бизнес-логику и использует CRUD для доступа к данным.
"""
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

from ..crud import crud_quiz_result, crud_quiz


class QuizResultService:
    """Сервис для работы с результатами квизов"""

    def __init__(self, db: Session):
        self.db = db

    # ========== ПОЛУЧЕНИЕ ДАННЫХ ==========

    def get_user_results(self, user_id: int, quiz_id: Optional[int] = None) -> List[Dict]:
        """Получение результатов пользователя"""
        results = crud_quiz_result.get_user_results(self.db, user_id, quiz_id)
        return [self._result_to_dict(r) for r in results]

    def get_quiz_leaderboard(self, quiz_id: int, limit: int = 100) -> List[Dict]:
        """Получение таблицы лидеров для квиза"""
        if not crud_quiz.get_quiz(self.db, quiz_id):
            return []
        return crud_quiz_result.get_quiz_leaderboard(self.db, quiz_id, limit)

    def get_user_statistics(self, user_id: int) -> Dict[str, Any]:
        """Получение статистики пользователя"""
        return crud_quiz_result.get_user_statistics(self.db, user_id)

    # ========== СОЗДАНИЕ РЕЗУЛЬТАТОВ ==========

    def save_result(
            self,
            user_id: int,
            quiz_id: int,
            score: int,
            max_score: int,
            is_completed: bool = True,
            duration_seconds: int = 0
    ) -> Dict:
        """Сохранение результата квиза"""
        result = crud_quiz_result.save_quiz_result(
            self.db,
            user_id=user_id,
            quiz_id=quiz_id,
            score=score,
            max_score=max_score,
            is_completed=is_completed,
            duration_seconds=duration_seconds
        )
        return self._result_to_dict(result)

    # ========== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ==========

    def check_quiz_exists(self, quiz_id: int) -> bool:
        """Проверка существования квиза"""
        return crud_quiz.get_quiz(self.db, quiz_id) is not None

    # ========== ПРЕОБРАЗОВАНИЯ ==========

    def _result_to_dict(self, result) -> Dict:
        """Преобразование QuizResult в dict для ответа"""
        return {
            "id": result.id,
            "user_id": result.user_id,
            "quiz_id": result.quiz_id,
            "score": result.score,
            "max_score": result.max_score,
            "percentage": result.percentage if hasattr(result, 'percentage') else (result.score / result.max_score * 100 if result.max_score else 0),
            "is_completed": result.is_completed,
            "duration_seconds": result.duration_seconds,
            "started_at": result.started_at.isoformat() if result.started_at else None,
            "completed_at": result.completed_at.isoformat() if result.completed_at else None,
        }
