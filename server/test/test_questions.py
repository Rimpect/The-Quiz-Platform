"""
Тесты для вопросов
"""
from .conftest import check_response_format


class TestQuestions:
    """Тесты вопросов"""

    def test_create_question(self, client, test_token, test_quiz):
        """Создание вопроса"""
        response = client.post(
            f"/api/quizzes/{test_quiz.id}/questions",
            headers={"Authorization": f"Bearer {test_token}"},
            json={
                "answer_type": "single",
                "points": 10,
                "question_text": "Test question?",
                "time_limit_seconds": 30
            }
        )
        assert response.status_code == 200
        data = check_response_format(response)
        assert data["data"]["question_text"] == "Test question?"
        assert data["data"]["points"] == 10
        assert "id" in data["data"]

    def test_create_question_without_auth(self, client, test_quiz):
        """Создание вопроса без авторизации (должен быть 401)"""
        response = client.post(
            f"/api/quizzes/{test_quiz.id}/questions",
            json={
                "answer_type": "single",
                "points": 10,
                "question_text": "Test question?",
                "time_limit_seconds": 30
            }
        )
        assert response.status_code == 401
        data = check_response_format(response)
        assert data["access_status"] == "missing"

    def test_get_questions_by_quiz(self, client, test_quiz, test_question):
        """Получение вопросов квиза"""
        response = client.get(f"/api/quizzes/{test_quiz.id}/questions")
        assert response.status_code == 200
        data = check_response_format(response)
        assert isinstance(data["data"], list)
        assert len(data["data"]) >= 1

    def test_get_question_by_id(self, client, test_quiz, test_question):
        """Получение вопроса по ID"""
        response = client.get(
            f"/api/quizzes/{test_quiz.id}/questions/{test_question.id}"
        )
        assert response.status_code == 200
        data = check_response_format(response)
        assert data["data"]["id"] == test_question.id
        assert data["data"]["question_text"] == test_question.question_text

    def test_get_nonexistent_question(self, client, test_quiz):
        """Получение несуществующего вопроса"""
        response = client.get(f"/api/quizzes/{test_quiz.id}/questions/99999")
        assert response.status_code == 404
        data = check_response_format(response)
        assert data["status"] == "not_found"

    def test_update_question(self, client, test_token, test_quiz, test_question):
        """Обновление вопроса"""
        response = client.put(
            f"/api/quizzes/{test_quiz.id}/questions/{test_question.id}",
            headers={"Authorization": f"Bearer {test_token}"},
            json={"points": 20}
        )
        assert response.status_code == 200
        data = check_response_format(response)
        assert data["data"]["points"] == 20

    def test_update_question_incorrect_quiz(self, client, test_token, test_question):
        """Обновление вопроса с указанием неверного quiz_id"""
        response = client.put(
            f"/api/quizzes/99999/questions/{test_question.id}",
            headers={"Authorization": f"Bearer {test_token}"},
            json={"points": 20}
        )
        assert response.status_code == 404

    def test_delete_question(self, client, test_token, test_quiz, test_question):
        """Удаление вопроса"""
        response = client.delete(
            f"/api/quizzes/{test_quiz.id}/questions/{test_question.id}",
            headers={"Authorization": f"Bearer {test_token}"}
        )
        assert response.status_code == 200
        data = check_response_format(response)
        assert data["status"] == "success"

    def test_delete_already_deleted_question(self, client, test_token, test_quiz, test_question):
        """Удаление уже удалённого вопроса"""
        # Сначала удаляем
        client.delete(
            f"/api/quizzes/{test_quiz.id}/questions/{test_question.id}",
            headers={"Authorization": f"Bearer {test_token}"}
        )
        # Пытаемся удалить снова
        response = client.delete(
            f"/api/quizzes/{test_quiz.id}/questions/{test_question.id}",
            headers={"Authorization": f"Bearer {test_token}"}
        )
        assert response.status_code == 404

    def test_create_question_with_invalid_type(self, client, test_token, test_quiz):
        """Создание вопроса с неверным типом ответа"""
        response = client.post(
            f"/api/quizzes/{test_quiz.id}/questions",
            headers={"Authorization": f"Bearer {test_token}"},
            json={
                "answer_type": "invalid_type",
                "points": 10,
                "question_text": "Test question?",
                "time_limit_seconds": 30
            }
        )
        assert response.status_code == 422  # Validation error

    def test_create_question_without_required_fields(self, client, test_token, test_quiz):
        """Создание вопроса без обязательных полей"""
        response = client.post(
            f"/api/quizzes/{test_quiz.id}/questions",
            headers={"Authorization": f"Bearer {test_token}"},
            json={}
        )
        assert response.status_code == 422

    def test_create_multiple_questions_bulk(self, client, test_token, test_quiz):
        """Массовое создание вопросов (через bulk эндпоинт)"""
        response = client.post(
            f"/api/quizzes/{test_quiz.id}/questions/bulk",
            headers={"Authorization": f"Bearer {test_token}"},
            json=[
                {
                    "answer_type": "single",
                    "points": 10,
                    "question_text": "Bulk question 1",
                    "answers": [
                        {"answer_text": "Answer 1", "is_correct": True}
                    ]
                },
                {
                    "answer_type": "multiple",
                    "points": 20,
                    "question_text": "Bulk question 2",
                    "answers": [
                        {"answer_text": "Answer A", "is_correct": True},
                        {"answer_text": "Answer B", "is_correct": True}
                    ]
                }
            ]
        )
        assert response.status_code == 200
        data = check_response_format(response)
        assert "questions" in data["data"]
        assert len(data["data"]["questions"]) == 2