"""
Тесты для аутентификации
"""
import pytest
from .conftest import check_response_format


class TestAuth:
    """Тесты аутентификации"""

    def test_register_success(self, client):
        """Успешная регистрация пользователя"""
        response = client.post("/api/users/", json={
            "nickname": "NewUser",
            "email": "newuser@example.com",
            "password": "newpass123",
            "theme_site": "light"
        })
        assert response.status_code == 200
        data = check_response_format(response)
        assert data["status"] == "success"
        assert data["data"]["email"] == "newuser@example.com"
        assert "id" in data["data"]

    def test_register_duplicate_email(self, client, test_user):
        """Регистрация с уже существующим email"""
        response = client.post("/api/users/", json={
            "nickname": "AnotherUser",
            "email": "test@example.com",
            "password": "pass123",
            "theme_site": "light"
        })
        assert response.status_code == 400
        data = check_response_format(response)
        assert data["status"] == "bad_request"

    def test_login_success(self, client, test_user):
        """Успешный вход"""
        response = client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "testpass123"
        })
        assert response.status_code == 200
        data = check_response_format(response)
        assert data["access_status"] == "granted"
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]

    def test_login_wrong_password(self, client, test_user):
        """Вход с неверным паролем"""
        response = client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        data = check_response_format(response)
        assert data["access_status"] in ["denied", "invalid"]

    def test_verify_token_success(self, client, test_token):
        """Проверка валидного токена"""
        response = client.get(
            "/api/auth/verify",
            headers={"Authorization": f"Bearer {test_token}"}
        )
        assert response.status_code == 200
        data = check_response_format(response)
        assert data["access_status"] == "granted"

    def test_verify_token_invalid(self, client):
        """Проверка невалидного токена"""
        response = client.get(
            "/api/auth/verify",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
        data = check_response_format(response)
        assert data["access_status"] in ["invalid", "expired"]

    def test_access_protected_endpoint_without_token(self, client):
        """Доступ к защищённому эндпоинту без токена"""
        response = client.get("/api/users/me")
        assert response.status_code == 401
        data = check_response_format(response)
        assert data["access_status"] == "missing"