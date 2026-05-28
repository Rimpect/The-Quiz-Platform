"""
Тесты для ответов
"""
import pytest


class TestAnswers :
    """Тесты ответов"""

    def test_create_answer(self, client, test_token, test_question) :
        """Создание ответа"""
        response = client.post(
            f"/api/questions/{test_question.id}/answers",
            headers={"Authorization" : f"Bearer {test_token}"},
            json={
                "answer_text" : "Test answer",
                "is_correct" : True,
                "order_number" : 1
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["answer_text"] == "Test answer"
        assert data["is_correct"] == True

    def test_create_answers_bulk(self, client, test_token, test_question) :
        """Массовое создание ответов"""
        response = client.post(
            f"/api/questions/{test_question.id}/answers/bulk",
            headers={"Authorization" : f"Bearer {test_token}"},
            json=[
                {"answer_text" : "Option A", "is_correct" : False, "order_number" : 1},
                {"answer_text" : "Option B", "is_correct" : True, "order_number" : 2},
                {"answer_text" : "Option C", "is_correct" : False, "order_number" : 3}
            ]
        )
        assert response.status_code == 201
        data = response.json()
        assert len(data) == 3

    def test_get_answers_by_question(self, client, test_question, test_answers) :
        """Получение ответов вопроса"""
        response = client.get(f"/api/questions/{test_question.id}/answers")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3

    def test_update_answer(self, client, test_token, test_question, test_answers) :
        """Обновление ответа"""
        answer_id = test_answers[0].id
        response = client.put(
            f"/api/questions/{test_question.id}/answers/{answer_id}",
            headers={"Authorization" : f"Bearer {test_token}"},
            json={"answer_text" : "Updated answer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["answer_text"] == "Updated answer"

    def test_delete_answer(self, client, test_token, test_question, test_answers) :
        """Удаление ответа"""
        answer_id = test_answers[0].id
        response = client.delete(
            f"/api/questions/{test_question.id}/answers/{answer_id}",
            headers={"Authorization" : f"Bearer {test_token}"}
        )
        assert response.status_code == 204