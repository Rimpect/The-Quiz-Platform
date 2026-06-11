"""
Тесты для квизов
"""
import pytest
from .conftest import check_response_format


class TestQuizzes:
    """Тесты квизов"""

    def test_create_quiz(self, client, test_token, test_category):
        """Создание квиза"""
        response = client.post(
            "/api/quizzes/",
            headers={"Authorization": f"Bearer {test_token}"},
            json={
                "title": "New Quiz",
                "category_id": test_category.id,
                "description": "Quiz description",
                "is_public": True,
                "quiz_mode": "single"
            }
        )
        assert response.status_code == 200
        data = check_response_format(response)
        assert data["data"]["title"] == "New Quiz"
        assert "id" in data["data"]

    def test_get_quizzes_list(self, client):
        """Получение списка квизов"""
        response = client.get("/api/quizzes/")
        assert response.status_code == 200
        data = check_response_format(response)
        assert isinstance(data["data"], list)

    def test_get_quiz_by_id(self, client, test_quiz):
        """Получение квиза по ID"""
        response = client.get(f"/api/quizzes/{test_quiz.id}")
        assert response.status_code == 200
        data = check_response_format(response)
        assert data["data"]["id"] == test_quiz.id

    def test_get_quiz_categories(self, client):
        """Получение категорий квизов"""
        response = client.get("/api/quizzes/categories")
        assert response.status_code == 200
        data = check_response_format(response)
        assert "categories" in data["data"]

    def test_update_quiz(self, client, test_token, test_quiz):
        """Обновление квиза"""
        response = client.put(
            f"/api/quizzes/{test_quiz.id}",
            headers={"Authorization": f"Bearer {test_token}"},
            json={"title": "Updated Quiz Title"}
        )
        assert response.status_code == 200
        data = check_response_format(response)
        assert data["data"]["title"] == "Updated Quiz Title"

    def test_delete_quiz(self, client, test_token, test_quiz):
        """Удаление квиза"""
        response = client.delete(
            f"/api/quizzes/{test_quiz.id}",
            headers={"Authorization": f"Bearer {test_token}"}
        )
        assert response.status_code == 200
        data = check_response_format(response)
        assert data["status"] == "success"
    
    def test_get_nonexistent_quiz(self, client):
        """Получение несуществующего квиза"""
        response = client.get("/api/quizzes/99999")
        assert response.status_code == 404
        data = check_response_format(response)
        assert data["status"] == "not_found"