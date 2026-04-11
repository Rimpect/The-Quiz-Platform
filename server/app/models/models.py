from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base
import enum


# ========== Перечисления (Enums) ==========
class ThemeMode(str, enum.Enum) :
    LIGHT = "light"
    DARK = "dark"


class QuizMode(str, enum.Enum) :
    SINGLE = "single"  # Одиночный режим
    TEAM = "team"  # Командный режим


class AnswerType(str, enum.Enum) :
    SINGLE = "single"  # Одиночный выбор
    MULTIPLE = "multiple"  # Множественный выбор
    TEXT = "text"  # Текстовый ответ
    NUMERIC = "numeric"  # Числовой ответ


# ========== 1. Пользователь ==========
class User(Base) :
    __tablename__ = "users"

    # Обязательные поля
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50), nullable=False)  # Никнейм
    theme_site = Column(SQLEnum(ThemeMode), default=ThemeMode.LIGHT, nullable=False)  # Тема сайта
    photo_profile = Column(String(500), nullable=True)  # Фото профиля (путь к файлу)
    login = Column(String(50), unique=True, nullable=False, index=True)  # Логин
    email = Column(String(100), unique=True, nullable=False, index=True)  # Почта
    password_hash = Column(String(255), nullable=False)  # Пароль (хеш)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # Дата регистрации
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)  # Дата изменения

    # Связи
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    quiz_results = relationship("QuizResult", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) :
        return f"<User {self.login}>"


# ========== 2. JWT токен ==========
class RefreshToken(Base) :
    __tablename__ = "refresh_tokens"

    # Обязательные поля
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)  # ID пользователя
    refresh_token_hash = Column(String(255), nullable=False, unique=True)  # Refresh токен (хеш)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # Дата создания

    # Дополнительные поля для безопасности (опционально, но рекомендую)
    expires_at = Column(DateTime(timezone=True), nullable=False)  # Дата истечения
    revoked_at = Column(DateTime(timezone=True), nullable=True)  # Дата отзыва
    user_agent = Column(String(500), nullable=True)  # Информация об устройстве
    ip_address = Column(String(45), nullable=True)  # IP адрес

    # Связи
    user = relationship("User", back_populates="refresh_tokens")

    def __repr__(self) :
        return f"<RefreshToken user_id={self.user_id}>"


# ========== 3. Квиз ==========
class Quiz(Base) :
    __tablename__ = "quizzes"

    # Обязательные поля
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)  # Название
    category = Column(String(100), nullable=False)  # Категория
    description = Column(Text, nullable=False)  # Описание
    cover_url = Column(String(500), nullable=True)  # Обложка (путь к файлу)
    is_public = Column(Boolean, default=True, nullable=False)  # Публичность квиза
    quiz_mode = Column(SQLEnum(QuizMode), default=QuizMode.SINGLE, nullable=False)  # Режим команды
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # Дата создания
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)  # Дата изменения

    # Вычисляемые поля (НЕ сохраняются в БД!)
    # duration_minutes - вычисляется из вопросов
    # total_questions - вычисляется из вопросов
    # difficulty - вычисляется на основе вопросов
    # times_taken - вычисляется из статистики прохождений

    # Связи
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    results = relationship("QuizResult", back_populates="quiz", cascade="all, delete-orphan")

    # Вычисляемые свойства (property)
    @property
    def total_questions(self) -> int :
        """Количество вопросов в квизе"""
        return len(self.questions) if self.questions else 0

    @property
    def duration_minutes(self) -> int :
        """Длительность квиза в минутах (сумма времени ожидания ответа на все вопросы)"""
        if not self.questions :
            return 0
        total_seconds = sum(q.time_limit_seconds for q in self.questions if q.time_limit_seconds)
        return total_seconds // 60  # Переводим в минуты

    @property
    def difficulty(self) -> str :
        """Сложность квиза (среднее арифметическое сложности вопросов)"""
        if not self.questions :
            return "easy"
        # Если у вас есть поле difficulty в вопросах, можно усреднять
        # Пока возвращаем среднее значение на основе баллов
        avg_points = sum(q.points for q in self.questions) / len(self.questions)
        if avg_points <= 2 :
            return "easy"
        elif avg_points <= 5 :
            return "medium"
        else :
            return "hard"

    @property
    def times_taken(self) -> int :
        """Количество прохождений квиза"""
        return len(self.results) if self.results else 0

    def __repr__(self) :
        return f"<Quiz {self.title}>"


# ========== 4. Вопрос ==========
class Question(Base) :
    __tablename__ = "questions"

    # Обязательные поля
    id = Column(Integer, primary_key=True, index=True)
    answer_type = Column(SQLEnum(AnswerType), nullable=False)  # Тип внесения ответа
    points = Column(Integer, default=1, nullable=False)  # Количество баллов
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # Дата создания
    question_text = Column(Text, nullable=False)  # Содержание вопроса
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)  # Дата изменения
    media_url = Column(String(500), nullable=True)  # Медиа (путь к файлу)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)  # ID квиза
    time_limit_seconds = Column(Integer, nullable=True)  # Время ожидания ответа (в секундах)

    # Связи
    quiz = relationship("Quiz", back_populates="questions")
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")
    user_answers = relationship("UserAnswer", back_populates="question", cascade="all, delete-orphan")

    def __repr__(self) :
        return f"<Question {self.id}: {self.question_text[:50]}>"


# ========== 5. Ответ (варианты ответов) ==========
class Answer(Base) :
    __tablename__ = "answers"

    # Обязательные поля
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False,
                         index=True)  # ID вопроса
    answer_text = Column(Text, nullable=False)  # Текст ответа
    is_correct = Column(Boolean, default=False, nullable=False)  # Правильный ли ответ

    # Дополнительное поле для порядка отображения (опционально)
    order_number = Column(Integer, default=0)  # Порядок отображения вариантов

    # Связи
    question = relationship("Question", back_populates="answers")
    user_selected_answers = relationship("UserAnswer", back_populates="selected_answer")

    def __repr__(self) :
        return f"<Answer {self.id}: {self.answer_text[:30]}>"


# ========== 6. Статистика прохождений ==========
class QuizResult(Base) :
    __tablename__ = "quiz_results"

    # Сохраняемые поля
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)  # ID пользователя
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)  # ID квиза
    score = Column(Float, nullable=False)  # Полученные баллы
    is_completed = Column(Boolean, default=False, nullable=False)  # Пройден ли полностью
    max_score = Column(Float, nullable=False)  # Максимально возможные баллы
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # Дата старта
    completed_at = Column(DateTime(timezone=True), nullable=True)  # Дата прохождения

    # Вычисляемое поле (НЕ сохраняется)
    # duration_seconds - вычисляется как разница между completed_at и started_at

    # Связи
    user = relationship("User", back_populates="quiz_results")
    quiz = relationship("Quiz", back_populates="results")
    user_answers = relationship("UserAnswer", back_populates="quiz_result", cascade="all, delete-orphan")

    # Вычисляемые свойства
    @property
    def duration_seconds(self) -> int :
        """Время прохождения в секундах (вычисляемое)"""
        if self.completed_at and self.started_at :
            delta = self.completed_at - self.started_at
            return int(delta.total_seconds())
        return 0

    @property
    def percentage(self) -> float :
        """Процент правильных ответов"""
        if self.max_score > 0 :
            return (self.score / self.max_score) * 100
        return 0.0

    def __repr__(self) :
        return f"<QuizResult user={self.user_id}, quiz={self.quiz_id}, score={self.score}>"


# ========== 7. Детальные ответы пользователя (дополнительная таблица) ==========
# Эта таблица не была в вашем описании, но она необходима для хранения
# конкретных ответов пользователя на каждый вопрос
class UserAnswer(Base) :
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True, index=True)
    quiz_result_id = Column(Integer, ForeignKey("quiz_results.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)

    # Ответ пользователя
    answer_text = Column(Text, nullable=True)  # Для текстовых ответов
    answer_id = Column(Integer, ForeignKey("answers.id"), nullable=True)  # Для выбранного варианта
    is_correct = Column(Boolean, default=False, nullable=False)
    points_earned = Column(Integer, default=0, nullable=False)

    # Метаданные
    time_spent_seconds = Column(Integer, nullable=True)  # Время затраченное на вопрос

    # Связи
    quiz_result = relationship("QuizResult", back_populates="user_answers")
    question = relationship("Question", back_populates="user_answers")
    selected_answer = relationship("Answer", back_populates="user_selected_answers")