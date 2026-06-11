"""
pytest конфигурация и фикстуры для тестирования
"""
from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from ..app.database.database import Base, get_db
from ..app.main import app

# Тестовая база данных SQLite (in-memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db?check_same_thread=False"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Переопределение зависимости get_db для тестов"""
    try:
        db: Session = TestingSessionLocal()
        yield db
    finally:
        db.close()


....dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def db() -> Generator[Session, None, None]:
    """Фикстура для сессии БД"""
    # Создаём таблицы
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

    # Очищаем после тестов
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client() -> Generator:
    """Фикстура для тестового клиента"""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_user(db: Session):
    """Фикстура для создания тестового пользователя"""
    from ..app.crud import crud_user as user_crud
    from ..app.schemas.schemas_user import UserCreate

    user_data = UserCreate(
        nickname="TestUser",
        email="test@example.com",
        password="testpass123",
        theme_site="light"
    )

    existing_user = user_crud.get_user_by_email(db, "test@example.com")
    if existing_user:
        return existing_user

    user = user_crud.create_user(db=db, user=user_data)
    return user


@pytest.fixture
def test_admin_user(db: Session):
    """Фикстура для создания тестового администратора"""
    from ..app.crud import crud_user as user_crud
    from ..app.schemas.schemas_user import UserCreate

    user_data = UserCreate(
        nickname="AdminUser",
        email="admin@example.com",
        password="adminpass123",
        theme_site="light"
    )

    existing_user = user_crud.get_user_by_email(db, "admin@example.com")
    if existing_user:
        existing_user.role = "admin"
        db.commit()
        return existing_user

    user = user_crud.create_user(db=db, user=user_data)
    user.role = "admin"
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_guest(db: Session, client):
    """Фикстура для создания гостя через API"""
    response = client.post("/api/guest/register", json={
        "nickname": "TestGuest",
        "expires_hours": 24
    })
    if response.status_code == 200:
        data = response.json()
        return data.get("data", {})
    return None


@pytest.fixture
def test_token(client, test_user):
    """Фикстура для получения access токена"""
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    if response.status_code == 200:
        data = response.json()
        return data.get("data", {}).get("access_token")
    return None


@pytest.fixture
def auth_headers(test_token):
    """Фикстура для заголовков с авторизацией"""
    return {"Authorization": f"Bearer {test_token}"}


@pytest.fixture
def test_category(db: Session):
    """Фикстура для создания тестовой категории"""
    from ..app.crud.crud_categories import Category as category_crud

    category = category_crud.get_category_by_type(db, "Test Category")
    if not category:
        category = category_crud.create_category(db, "Test Category", "Test description")
    return category


@pytest.fixture
def test_quiz(db: Session, test_user, test_category):
    """Фикстура для создания тестового квиза"""
    from ..app.crud import crud_quiz as quiz_crud
    from ..app.schemas.schemas_quiz import QuizCreate

    quiz_data = QuizCreate(
        title="Test Quiz",
        category_id=test_category.id,
        description="This is a test quiz",
        is_public=True,
        quiz_mode="single"
    )

    quiz = quiz_crud.create_quiz(db=db, quiz=quiz_data)
    return quiz


@pytest.fixture
def test_question(db: Session, test_quiz):
    """Фикстура для создания тестового вопроса"""
    from ..app.crud import crud_question as question_crud
    from ..app.schemas.schemas_question import QuestionCreate

    question_data = QuestionCreate(
        answer_type="single",
        points=10,
        question_text="What is 2+2?",
        time_limit_seconds=30
    )

    question = question_crud.create_question(
        db=db,
        question=question_data,
        quiz_id=test_quiz.id
    )
    return question


@pytest.fixture
def test_answers(db: Session, test_question):
    """Фикстура для создания тестовых ответов"""
    from ..app.crud.crud_answer import Answer as answer_crud
    from ..app.schemas.schemas_answer import AnswerCreate
    
    answers_data = [
        AnswerCreate(answer_text="3", is_correct=False, order_number=1),
        AnswerCreate(answer_text="4", is_correct=True, order_number=2),
        AnswerCreate(answer_text="5", is_correct=False, order_number=3),
    ]
    
    answers = answer_crud.create_answers_bulk(
        db=db, 
        answers=answers_data, 
        question_id=test_question.id
    )
    return answers


def check_response_format(response):
    """Вспомогательная функция для проверки формата ответа"""
    data = response.json()
    assert "status_code" in data
    assert "status" in data
    assert "access_status" in data
    assert "message" in data
    assert "timestamp" in data
    return data