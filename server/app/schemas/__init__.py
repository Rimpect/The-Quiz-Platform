"""
Schemas модуль - экспорт всех Pydantic моделей
"""

# Response
from .schemas_response import (
    BaseResponse,
    PaginatedResponse,
    ErrorResponse,
    ResponseFactory,
    AccessStatus,
    ResponseStatus
)

# User
from .schemas_user import (
    User,
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    GuestCreate,
    GuestResponse,
    PromoteGuestRequest,
    Token,
    EmailRequest,
    RefreshTokenRequest,
    EmailResponse,
    RefreshTokenResponse,
    AccessTokenStatusResponse
)

# Quiz & Category
from .schemas_quiz import (
    CategoryBase,
    CategoryCreate,
    CategoryUpdate,
    Category,
    CategoryWithStats,
    QuizBase,
    QuizCreate,
    QuizUpdate,
    QuizResponse,
    QuizBulkCreate,
    QuestionBulkCreate,
    AnswerBulkCreate,
    QuizBulkResponse
)

# Question
from .schemas_question import (
    QuestionBase,
    QuestionCreate,
    QuestionUpdate,
    QuestionResponse
)

# Answer
from .schemas_answer import (
    AnswerBase,
    AnswerCreate,
    AnswerUpdate,
    AnswerResponse
)

# Quiz Result
from .schemas_quiz_result import (
    QuizResultBase,
    QuizResultCreate,
    QuizResultUpdate,
    QuizResultResponse
)

# User Answer (Redis)
from .schemas_user_answer import (
    UserAnswerCreate,
    UserAnswerUpdate,
    UserAnswerResponse,
    SessionScoreResponse,
    StartSessionResponse
)

# Lobby & Session
from .schemas_lobby import (
    LobbyCreate,
    LobbyResponse,
    JoinLobbyRequest,
    StartGameResponse
)

__all__ = [
    # Response
    "BaseResponse",
    "PaginatedResponse",
    "ErrorResponse",
    "ResponseFactory",
    "AccessStatus",
    "ResponseStatus",

    # User
    "User",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "GuestCreate",
    "GuestResponse",
    "PromoteGuestRequest",
    "Token",
    "EmailRequest",
    "RefreshTokenRequest",
    "AccessTokenStatusResponse",

    # Quiz
    "CategoryBase",
    "CategoryCreate",
    "CategoryUpdate",
    "Category",
    "CategoryWithStats",
    "QuizBase",
    "QuizCreate",
    "QuizUpdate",
    "QuizResponse",
    "QuizBulkCreate",
    "QuestionBulkCreate",
    "AnswerBulkCreate",
    "QuizBulkResponse",

    # Question
    "QuestionBase",
    "QuestionCreate",
    "QuestionUpdate",
    "QuestionResponse",

    # Answer
    "AnswerBase",
    "AnswerCreate",
    "AnswerUpdate",
    "AnswerResponse",

    # Quiz Result
    "QuizResultBase",
    "QuizResultCreate",
    "QuizResultUpdate",
    "QuizResultResponse",

    # User Answer
    "UserAnswerCreate",
    "UserAnswerUpdate",
    "UserAnswerResponse",
    "SessionScoreResponse",
    "StartSessionResponse",

    # Lobby
    "LobbyCreate",
    "LobbyResponse",
    "JoinLobbyRequest",
    "StartGameResponse"
]
