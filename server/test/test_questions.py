"""
Тесты для вопросов
"""
import pytest


class TestQuestions :
    """Тесты вопросов"""

    def test_create_question(self, client, test_token, test_quiz) :
        """Создание вопроса"""
        response = client.post(
            f"/api/quizzes/{test_quiz.id}/questions",
            headers={"Authorization" : f"Bearer {test_token}"},
            json={
                "answer_type" : "single",
                "points" : 10,
                "question_text" : "Test question?",
                "time_limit_seconds" : 30
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["question_text"] == "Test question?"
        assert data["points"] == 10

    def test_get_questions_by_quiz(self, client, test_quiz, test_question) :
        """Получение вопросов квиза"""
        response = client.get(f"/api/quizzes/{test_quiz.id}/questions")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_get_question_by_id(self, client, test_quiz, test_question) :
        """Получение вопроса по ID"""
        response = client.get(
            f"/api/quizzes/{test_quiz.id}/questions/{test_question.id}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_question.id

    def test_update_question(self, client, test_token, test_quiz, test_question) :
        """Обновление вопроса"""
        response = client.put(
            f"/api/quizzes/{test_quiz.id}/questions/{test_question.id}",
            headers={"Authorization" : f"Bearer {test_token}"},
            json={"points" : 20}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["points"] == 20

    def test_delete_question(self, client, test_token, test_quiz, test_question) :
        """Удаление вопроса"""
        response = client.delete(
            f"/api/quizzes/{test_quiz.id}/questions/{test_question.id}",
            headers={"Authorization" : f"Bearer {test_token}"}
        )
        assert response.status_code == 204