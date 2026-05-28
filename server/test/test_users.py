"""
Тесты для пользователей
"""
import pytest


class TestUsers :
    """Тесты пользователей"""

    def test_get_current_user(self, client, test_token) :
        """Получение текущего пользователя"""
        response = client.get(
            "/api/users/me",
            headers={"Authorization" : f"Bearer {test_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["login"] == "testuser"
        assert data["email"] == "test@example.com"

    def test_get_user_by_id(self, client, test_token, test_user) :
        """Получение пользователя по ID"""
        response = client.get(
            f"/api/users/{test_user.id}",
            headers={"Authorization" : f"Bearer {test_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user.id

    def test_update_current_user(self, client, test_token) :
        """Обновление текущего пользователя"""
        response = client.put(
            "/api/users/me",
            headers={"Authorization" : f"Bearer {test_token}"},
            json={"nickname" : "UpdatedNickname"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["nickname"] == "UpdatedNickname"

    def test_get_user_statistics(self, client, test_token) :
        """Получение статистики пользователя"""
        response = client.get(
            "/api/users/me/statistics",
            headers={"Authorization" : f"Bearer {test_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "total_quizzes_completed" in data
        assert "average_score" in data

    def test_delete_current_user(self, client, test_token) :
        """Удаление текущего пользователя"""
        response = client.delete(
            "/api/users/me",
            headers={"Authorization" : f"Bearer {test_token}"}
        )
        assert response.status_code == 204