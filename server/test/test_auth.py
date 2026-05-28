"""
Тесты для аутентификации
"""
import pytest
from app.utils.security import get_password_hash, verify_password


class TestAuth :
    """Тесты аутентификации"""

    def test_register_success(self, client) :
        """Успешная регистрация пользователя"""
        response = client.post("/api/users/", json={
            "nickname" : "NewUser",
            "login" : "newuser",
            "email" : "newuser@example.com",
            "password" : "newpass123",
            "theme_site" : "light"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["login"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "id" in data

    def test_register_duplicate_login(self, client, test_user) :
        """Регистрация с уже существующим логином"""
        response = client.post("/api/users/", json={
            "nickname" : "AnotherUser",
            "login" : "testuser",  # Уже существует
            "email" : "another@example.com",
            "password" : "pass123",
            "theme_site" : "light"
        })
        assert response.status_code == 400
        assert "already registered" in response.text.lower()

    def test_register_duplicate_email(self, client, test_user) :
        """Регистрация с уже существующим email"""
        response = client.post("/api/users/", json={
            "nickname" : "AnotherUser",
            "login" : "anotheruser",
            "email" : "test@example.com",  # Уже существует
            "password" : "pass123",
            "theme_site" : "light"
        })
        assert response.status_code == 400
        assert "already registered" in response.text.lower()

    def test_login_success(self, client, test_user) :
        """Успешный вход"""
        response = client.post("/api/auth/login", json={
            "login" : "testuser",
            "password" : "testpass123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_with_email(self, client, test_user) :
        """Вход с использованием email"""
        response = client.post("/api/auth/login", json={
            "login" : "test@example.com",
            "password" : "testpass123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    def test_login_wrong_password(self, client, test_user) :
        """Вход с неверным паролем"""
        response = client.post("/api/auth/login", json={
            "login" : "testuser",
            "password" : "wrongpassword"
        })
        assert response.status_code == 401
        assert "invalid credentials" in response.text.lower()

    def test_login_nonexistent_user(self, client) :
        """Вход с несуществующим пользователем"""
        response = client.post("/api/auth/login", json={
            "login" : "nonexistent",
            "password" : "pass123"
        })
        assert response.status_code == 401

    def test_verify_token_success(self, client, test_token) :
        """Проверка валидного токена"""
        response = client.get(
            "/api/auth/verify",
            headers={"Authorization" : f"Bearer {test_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] == True

    def test_verify_token_invalid(self, client) :
        """Проверка невалидного токена"""
        response = client.get(
            "/api/auth/verify",
            headers={"Authorization" : "Bearer invalid_token"}
        )
        assert response.status_code == 401

    def test_refresh_token_success(self, client, test_refresh_token) :
        """Обновление токена"""
        response = client.post("/api/auth/refresh", json={
            "refresh_token" : test_refresh_token
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_logout_success(self, client, test_token, test_refresh_token) :
        """Успешный выход"""
        response = client.post(
            "/api/auth/logout",
            headers={"Authorization" : f"Bearer {test_token}"},
            json={"refresh_token" : test_refresh_token}
        )
        assert response.status_code == 204

    def test_access_protected_endpoint_without_token(self, client) :
        """Доступ к защищенному эндпоинту без токена"""
        response = client.get("/api/users/me")
        assert response.status_code == 401