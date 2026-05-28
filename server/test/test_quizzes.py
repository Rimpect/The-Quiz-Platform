"""
Тесты для квизов
"""
import pytest


class TestQuizzes :
    """Тесты квизов"""

    def test_create_quiz(self, client, test_token) :
        """Создание квиза"""
        response = client.post(
            "/api/quizzes/",
            headers={"Authorization" : f"Bearer {test_token}"},
            json={
                "title" : "New Quiz",
                "category" : "General",
                "description" : "Quiz description",
                "is_public" : True,
                "quiz_mode" : "single"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Quiz"
        assert data["category"] == "General"
        assert "id" in data

    def test_get_quizzes_list(self, client) :
        """Получение списка квизов"""
        response = client.get("/api/quizzes/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_quiz_by_id(self, client, test_quiz) :
        """Получение квиза по ID"""
        response = client.get(f"/api/quizzes/{test_quiz.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_quiz.id
        assert data["title"] == test_quiz.title

    def test_get_quiz_categories(self, client) :
        """Получение категорий квизов"""
        response = client.get("/api/quizzes/categories")
        assert response.status_code == 200
        assert "categories" in response.json()

    def test_update_quiz(self, client, test_token, test_quiz) :
        """Обновление квиза"""
        response = client.put(
            f"/api/quizzes/{test_quiz.id}",
            headers={"Authorization" : f"Bearer {test_token}"},
            json={"title" : "Updated Quiz Title"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Quiz Title"

    def test_delete_quiz(self, client, test_token, test_quiz) :
        """Удаление квиза"""
        response = client.delete(
            f"/api/quizzes/{test_quiz.id}",
            headers={"Authorization" : f"Bearer {test_token}"}
        )
        assert response.status_code == 204

    def test_get_nonexistent_quiz(self, client) :
        """Получение несуществующего квиза"""
        response = client.get("/api/quizzes/99999")
        assert response.status_code == 404