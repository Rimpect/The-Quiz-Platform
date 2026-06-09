"""
Интеграционные тесты
"""


class TestIntegration:
    """Интеграционные тесты"""

    def test_full_quiz_flow(self, client, test_token, test_category):
        """Полный цикл: создание квиза → вопросы → ответы → прохождение"""

        # 1. Создание квиза
        quiz_response = client.post(
            "/api/quizzes/",
            headers={"Authorization": f"Bearer {test_token}"},
            json={
                "title": "Integration Test Quiz",
                "category_id": test_category.id,
                "description": "Testing full flow",
                "is_public": True,
                "quiz_mode": "single"
            }
        )
        assert quiz_response.status_code == 200
        quiz_data = quiz_response.json()["data"]
        quiz_id = quiz_data["id"]

        # 2. Создание вопроса
        question_response = client.post(
            f"/api/quizzes/{quiz_id}/questions",
            headers={"Authorization": f"Bearer {test_token}"},
            json={
                "answer_type": "single",
                "points": 10,
                "question_text": "What is the capital of France?",
                "time_limit_seconds": 30
            }
        )
        assert question_response.status_code == 200
        question_data = question_response.json()["data"]
        question_id = question_data["id"]

        # 3. Создание ответов
        answers_response = client.post(
            f"/api/questions/{question_id}/answers/bulk",
            headers={"Authorization": f"Bearer {test_token}"},
            json=[
                {"answer_text": "London", "is_correct": False, "order_number": 1},
                {"answer_text": "Berlin", "is_correct": False, "order_number": 2},
                {"answer_text": "Paris", "is_correct": True, "order_number": 3},
                {"answer_text": "Madrid", "is_correct": False, "order_number": 4}
            ]
        )
        assert answers_response.status_code == 200

        # 4. Получение квиза
        get_quiz_response = client.get(f"/api/quizzes/{quiz_id}")
        assert get_quiz_response.status_code == 200
        assert get_quiz_response.json()["data"]["title"] == "Integration Test Quiz"

        # 5. Получение вопросов
        get_questions_response = client.get(f"/api/quizzes/{quiz_id}/questions")
        assert get_questions_response.status_code == 200
        assert len(get_questions_response.json()["data"]) >= 1

    def test_user_registration_and_login_flow(self, client):
        """Полный цикл: регистрация → логин → получение профиля → выход"""

        # 1. Регистрация
        register_response = client.post("/api/users/", json={
            "nickname": "FlowTestUser",
            "email": "flow@example.com",
            "password": "flowpass123",
            "theme_site": "light"
        })
        assert register_response.status_code == 200

        # 2. Логин
        login_response = client.post("/api/auth/login", json={
            "email": "flow@example.com",
            "password": "flowpass123"
        })
        assert login_response.status_code == 200
        access_token = login_response.json()["data"]["access_token"]

        # 3. Получение профиля
        profile_response = client.get(
            "/api/users/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert profile_response.status_code == 200
        assert profile_response.json()["data"]["email"] == "flow@example.com"

        # 4. Выход
        logout_response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert logout_response.status_code == 200

    def test_guest_flow(self, client):
        """Полный цикл для гостя: регистрация → игра → преобразование в пользователя"""

        # 1. Регистрация гостя
        guest_response = client.post("/api/guest/register", json={
            "nickname": "GuestToUser",
            "expires_hours": 24
        })
        assert guest_response.status_code == 200
        guest_data = guest_response.json()["data"]
        guest_token = guest_data["access_token"]
        guest_id = guest_data["id"]

        # 2. Гость получает список квизов
        quizzes_response = client.get(
            "/api/quizzes/",
            headers={"Authorization": f"Bearer {guest_token}"}
        )
        assert quizzes_response.status_code == 200

        # 3. Преобразование гостя в пользователя
        promote_response = client.post("/api/guest/promote", json={
            "guest_id": guest_id,
            "login": "converted_user",
            "email": "converted@example.com",
            "password": "newpass123"
        })
        assert promote_response.status_code == 200

        # 4. Вход новым пользователем
        login_response = client.post("/api/auth/login", json={
            "email": "converted@example.com",
            "password": "newpass123"
        })
        assert login_response.status_code == 200

    def test_quiz_bulk_create_flow(self, client, test_token, test_category):
        """Массовое создание квиза с вопросами и ответами"""

        response = client.post(
            "/api/quizzes/bulk",
            headers={"Authorization": f"Bearer {test_token}"},
            json={
                "title": "Bulk Quiz",
                "category_id": test_category.id,
                "description": "Created via bulk endpoint",
                "is_public": True,
                "quiz_mode": "single",
                "questions": [
                    {
                        "answer_type": "single",
                        "points": 10,
                        "question_text": "Question 1",
                        "answers": [
                            {"answer_text": "Answer 1", "is_correct": True},
                            {"answer_text": "Answer 2", "is_correct": False}
                        ]
                    },
                    {
                        "answer_type": "multiple",
                        "points": 20,
                        "question_text": "Question 2",
                        "answers": [
                            {"answer_text": "Option A", "is_correct": True},
                            {"answer_text": "Option B", "is_correct": True},
                            {"answer_text": "Option C", "is_correct": False}
                        ]
                    }
                ]
            }
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["questions_created"] == 2
        assert data["answers_created"] == 5

    def test_copy_quiz_flow(self, client, test_token, test_quiz):
        """Копирование существующего квиза"""

        response = client.post(
            f"/api/quizzes/{test_quiz.id}/copy",
            headers={"Authorization": f"Bearer {test_token}"},
            params={"new_title": "Copied Quiz", "copy_questions": True}
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["title"] == "Copied Quiz"
        assert data["id"] != test_quiz.id

    def test_export_quiz_flow(self, client, test_token, test_quiz):
        """Экспорт квиза в JSON"""

        response = client.get(
            f"/api/quizzes/{test_quiz.id}/export",
            headers={"Authorization": f"Bearer {test_token}"}
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert "title" in data
        assert "questions" in data

    def test_category_management_flow(self, client, test_token, test_category):
        """Управление категориями (админ-функции)"""

        # 1. Создание новой категории
        create_response = client.post(
            "/api/categories/",
            headers={"Authorization": f"Bearer {test_token}"},
            json={"category_type": "New Category", "description": "Test description"}
        )
        assert create_response.status_code == 200
        category_data = create_response.json()["data"]
        category_id = category_data["id"]

        # 2. Получение всех категорий
        get_response = client.get("/api/categories/")
        assert get_response.status_code == 200
        categories = get_response.json()["data"]
        assert len(categories) >= 1

        # 3. Обновление категории
        update_response = client.put(
            f"/api/categories/{category_id}",
            headers={"Authorization": f"Bearer {test_token}"},
            json={"category_type": "Updated Category"}
        )
        assert update_response.status_code == 200

        # 4. Удаление категории
        delete_response = client.delete(
            f"/api/categories/{category_id}",
            headers={"Authorization": f"Bearer {test_token}"}
        )
        assert delete_response.status_code == 200

    def test_health_endpoints(self, client):
        """Проверка системных эндпоинтов"""

        # Health check
        health_response = client.get("/health")
        assert health_response.status_code == 200

        # Info
        info_response = client.get("/info")
        assert info_response.status_code == 200
        data = info_response.json()
        assert "name" in data
        assert "version" in data

        # Root
        root_response = client.get("/")
        assert root_response.status_code == 200