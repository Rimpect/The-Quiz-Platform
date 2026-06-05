"""
pytest конфигурация и фикстуры
"""
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool


from ..app.database.database import Base, get_db
from ..app.utils.security import get_password_hash
from ..app.models import User, Quiz, Question, Answer, JWTToken

# Тестовая база данных SQLite (in-memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db?check_same_thread=False"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread" : False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() :
    """Переопределение зависимости get_db для тестов"""
    try :
        db = TestingSessionLocal()
        yield db
    finally :
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def db() -> Generator[Session, None, None] :
    """Фикстура для сессии БД"""
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try :
        yield db
    finally :
        db.close()

    # Очищаем после тестов
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client() -> Generator :
    """Фикстура для тестового клиента"""
    with TestClient(app) as c :
        yield c


@pytest.fixture
def test_user(db: Session) :
    """Фикстура для создания тестового пользователя"""
    from ..app.crud import crud_user as crud_user
    from ..app.schemas import UserCreate

    user_data = UserCreate(
        nickname="TestUser",
        login="testuser",
        email="test@example.com",
        password="testpass123",
        theme_site="light"
    )

    # Проверяем, существует ли уже пользователь
    existing_user = crud_user.get_user_by_login(db, "testuser")
    if existing_user :
        return existing_user

    user = crud_user.create_user(db=db, user=user_data)
    return user


@pytest.fixture
def test_admin_user(db: Session) :
    """Фикстура для создания тестового администратора"""
    from ..app.crud import crud_user as crud_user
    from ..app.schemas import UserCreate

    user_data = UserCreate(
        nickname="AdminUser",
        login="adminuser",
        email="admin@example.com",
        password="adminpass123",
        theme_site="light"
    )

    existing_user = crud_user.get_user_by_login(db, "adminuser")
    if existing_user :
        return existing_user

    user = crud_user.create_user(db=db, user=user_data)
    # Обновляем роль до администратора
    user.role = "admin"
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_token(client, test_user) :
    """Фикстура для получения access токена"""
    response = client.post("/api/auth/login", json={
        "login" : "testuser",
        "password" : "testpass123"
    })
    return response.json().get("access_token")


@pytest.fixture
def test_refresh_token(client, test_user) :
    """Фикстура для получения refresh токена"""
    response = client.post("/api/auth/login", json={
        "login" : "testuser",
        "password" : "testpass123"
    })
    return response.json().get("refresh_token")


@pytest.fixture
def auth_headers(test_token) :
    """Фикстура для заголовков с авторизацией"""
    return {"Authorization" : f"Bearer {test_token}"}


@pytest.fixture
def test_quiz(db: Session, test_user) :
    """Фикстура для создания тестового квиза"""
    from ..app.crud import crud_quiz as crud_quiz
    from ..app.schemas import QuizCreate

    quiz_data = QuizCreate(
        title="Test Quiz",
        category="Testing",
        description="This is a test quiz",
        is_public=True,
        quiz_mode="single"
    )

    quiz = crud_quiz.create_quiz(db=db, quiz=quiz_data)
    return quiz


@pytest.fixture
def test_question(db: Session, test_quiz) :
    """Фикстура для создания тестового вопроса"""
    from ..app.crud import crud_question as crud_question
    from ..app.schemas import QuestionCreate

    question_data = QuestionCreate(
        answer_type="single",
        points=10,
        question_text="What is 2+2?",
        time_limit_seconds=30
    )

    question = crud_question.create_question(
        db=db,
        question=question_data,
        quiz_id=test_quiz.id
    )
    return question


@pytest.fixture
def test_answers(db: Session, test_question) :
    """Фикстура для создания тестовых ответов"""
    from ..app.crud import crud_answer as crud_answer
    from ..app.schemas import AnswerCreate

    answers_data = [
        AnswerCreate(answer_text="3", is_correct=False, order_number=1),
        AnswerCreate(answer_text="4", is_correct=True, order_number=2),
        AnswerCreate(answer_text="5", is_correct=False, order_number=3),
    ]

    answers = crud_answer.create_answers_bulk(
        db=db,
        answers=answers_data,
        question_id=test_question.id
    )
    return answers