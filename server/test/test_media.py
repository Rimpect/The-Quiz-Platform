"""
Тесты для медиафайлов
"""
import io

import pytest
from PIL import Image

from .conftest import check_response_format


class TestMedia :
    """Тесты медиафайлов"""

    @pytest.fixture
    def test_image(self) :
        """Создание тестового изображения"""
        file = io.BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(file, format='JPEG')
        file.name = 'test_image.jpg'
        file.seek(0)
        return file

    @pytest.fixture
    def test_large_file(self) :
        """Создание слишком большого файла"""
        return b'x' * (6 * 1024 * 1024)  # 6 MB

    def test_upload_profile_image(self, client, test_token, test_image) :
        """Загрузка изображения профиля"""
        response = client.post(
            "/api/media/upload/profile/1",
            headers={"Authorization" : f"Bearer {test_token}"},
            files={"file" : ("test.jpg", test_image, "image/jpeg")}
        )
        assert response.status_code == 200
        data = check_response_format(response)
        assert "url" in data["data"]
        assert data["data"]["file_name"] == "test.jpg"
        assert data["data"]["media_type"] == "image"

    def test_upload_without_auth(self, client, test_image) :
        """Загрузка файла без авторизации"""
        response = client.post(
            "/api/media/upload/profile/1",
            files={"file" : ("test.jpg", test_image, "image/jpeg")}
        )
        assert response.status_code == 401

    def test_upload_invalid_file_type(self, client, test_token) :
        """Загрузка файла недопустимого типа"""
        response = client.post(
            "/api/media/upload/profile/1",
            headers={"Authorization" : f"Bearer {test_token}"},
            files={"file" : ("test.txt", b"text content", "text/plain")}
        )
        assert response.status_code == 400
        data = check_response_format(response)
        assert "unsupported" in data["message"].lower()

    def test_upload_large_file(self, client, test_token, test_large_file) :
        """Загрузка слишком большого файла"""
        response = client.post(
            "/api/media/upload/profile/1",
            headers={"Authorization" : f"Bearer {test_token}"},
            files={"file" : ("large.jpg", test_large_file, "image/jpeg")}
        )
        assert response.status_code == 400
        data = check_response_format(response)
        assert "too large" in data["message"].lower()

    def test_get_media_file(self, client, test_token, test_image) :
        """Получение загруженного медиафайла"""
        # Сначала загружаем файл
        upload_response = client.post(
            "/api/media/upload/profile/1",
            headers={"Authorization" : f"Bearer {test_token}"},
            files={"file" : ("test.jpg", test_image, "image/jpeg")}
        )
        file_url = upload_response.json()["data"]["url"]

        # Получаем файл
        response = client.get(file_url)
        assert response.status_code == 200

    def test_get_entity_media(self, client, test_token, test_image, test_user) :
        """Получение всех медиафайлов сущности"""
        # Загружаем файл
        client.post(
            f"/api/media/upload/profile/{test_user.id}",
            headers={"Authorization" : f"Bearer {test_token}"},
            files={"file" : ("test.jpg", test_image, "image/jpeg")}
        )

        # Получаем список
        response = client.get(
            f"/api/media/entity/profile/{test_user.id}",
            headers={"Authorization" : f"Bearer {test_token}"}
        )
        assert response.status_code == 200
        data = check_response_format(response)
        assert isinstance(data["data"], list)
        assert len(data["data"]) >= 1

    def test_update_media_metadata(self, client, test_token, test_image, test_user) :
        """Обновление метаданных медиафайла"""
        # Загружаем файл
        upload_response = client.post(
            f"/api/media/upload/profile/{test_user.id}",
            headers={"Authorization" : f"Bearer {test_token}"},
            files={"file" : ("test.jpg", test_image, "image/jpeg")}
        )
        media_id = upload_response.json()["data"]["id"]

        # Обновляем метаданные
        response = client.put(
            f"/api/media/{media_id}",
            headers={"Authorization" : f"Bearer {test_token}"},
            json={"alt_text" : "Updated alt text", "order_number" : 5}
        )
        assert response.status_code == 200
        data = check_response_format(response)
        assert data["data"]["alt_text"] == "Updated alt text"
        assert data["data"]["order_number"] == 5

    def test_delete_media_file(self, client, test_token, test_image, test_user) :
        """Удаление медиафайла"""
        # Загружаем файл
        upload_response = client.post(
            f"/api/media/upload/profile/{test_user.id}",
            headers={"Authorization" : f"Bearer {test_token}"},
            files={"file" : ("test.jpg", test_image, "image/jpeg")}
        )
        media_id = upload_response.json()["data"]["id"]

        # Удаляем файл
        response = client.delete(
            f"/api/media/{media_id}",
            headers={"Authorization" : f"Bearer {test_token}"}
        )
        assert response.status_code == 200
        data = check_response_format(response)
        assert data["status"] == "success"

    def test_delete_nonexistent_media(self, client, test_token) :
        """Удаление несуществующего медиафайла"""
        response = client.delete(
            "/api/media/99999",
            headers={"Authorization" : f"Bearer {test_token}"}
        )
        assert response.status_code == 404

    def test_upload_multiple_files(self, client, test_token, test_user) :
        """Загрузка нескольких файлов одновременно"""
        files = [
            ("files", ("img1.jpg", b"content1", "image/jpeg")),
            ("files", ("img2.jpg", b"content2", "image/jpeg")),
            ("files", ("audio.mp3", b"audio", "audio/mpeg"))
        ]

        response = client.post(
            f"/api/media/upload-multiple/profile/{test_user.id}",
            headers={"Authorization" : f"Bearer {test_token}"},
            files=files
        )
        assert response.status_code == 200
        data = check_response_format(response)
        assert "uploaded_files" in data["data"]
        assert len(data["data"]["uploaded_files"]) == 3

    def test_delete_entity_all_media(self, client, test_token, test_image, test_user) :
        """Удаление всех медиафайлов сущности"""
        # Загружаем несколько файлов
        for i in range(3) :
            client.post(
                f"/api/media/upload/profile/{test_user.id}",
                headers={"Authorization" : f"Bearer {test_token}"},
                files={"file" : (f"test_{i}.jpg", test_image, "image/jpeg")}
            )

        # Удаляем все
        response = client.delete(
            f"/api/media/entity/profile/{test_user.id}",
            headers={"Authorization" : f"Bearer {test_token}"}
        )
        assert response.status_code == 200
        data = check_response_format(response)
        assert data["status"] == "success"