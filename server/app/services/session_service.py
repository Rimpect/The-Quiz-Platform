from sqlalchemy.orm import Session

from ..crud import crud_quiz as quiz_crud
from ..crud import crud_question as question_crud
from ..crud import crud_quiz_result as result_crud
from ..crud.crud_user_answer import user_answer_service
from ..models.model_user_answer import UserAnswer
from ..schemas.schemas_user_answer import StartSessionResponse, UserAnswerCreate
from ..config_redis.redis_service import QuizSessionService
from .exceptions import NotFoundError, ForbiddenError, BadRequestError

_redis_sessions = QuizSessionService()

def _require_own_session(session_id: str, user_id: int):
    session = _redis_sessions.get_session(session_id)
    if not session:
        raise NotFoundError("Session not found")
    if int(session.get("user_id")) != user_id:
        raise ForbiddenError("Not your session")
    return session

def start_session(db: Session, current_user, quiz_id: int):
    if not quiz_crud.get_quiz(db, quiz_id):
        raise NotFoundError("Quiz not found")

    questions = question_crud.get_questions_by_quiz(db, quiz_id)
    session_id = _redis_sessions.create_session(
        user_id=current_user.id, quiz_id=quiz_id, total_questions=len(questions)
    )
    return StartSessionResponse(
        session_id=session_id, quiz_id=quiz_id,
        total_questions=len(questions), expires_in_minutes=60,
    )

def start_guest_session(db: Session, current_guest, quiz_id: int):
    quiz = quiz_crud.get_quiz(db, quiz_id)
    if not quiz:
        raise NotFoundError("Quiz not found")
    if not quiz.is_public:
        raise ForbiddenError("Guests can only play public quizzes")

    questions = question_crud.get_questions_by_quiz(db, quiz_id)
    session_id = _redis_sessions.create_session(
        user_id=-current_guest.id, quiz_id=quiz_id, total_questions=len(questions)
    )
    return StartSessionResponse(
        session_id=session_id, quiz_id=quiz_id,
        total_questions=len(questions), expires_in_minutes=60,
    )

def save_answer(db: Session, current_user, session_id: str, answer: UserAnswerCreate):
    session = _require_own_session(session_id, current_user.id)

    question = question_crud.get_question(db, answer.question_id)
    if not question:
        raise NotFoundError("Question not found")
    if question.answer_type not in ["single", "multiple"]:
        raise BadRequestError("Invalid question type")

    result = user_answer_service.save_answer(
        session_id=session_id,
        user_id=current_user.id,
        quiz_id=int(session.get("quiz_id")),
        question_id=answer.question_id,
        answer_data=answer,
        db=db,
    )
    return {
        "message": "Answer saved",
        "is_correct": result["is_correct"],
        "points_earned": result["points_earned"],
    }

def get_session_answers(current_user, session_id: str):
    _require_own_session(session_id, current_user.id)
    return {"answers": user_answer_service.get_all_answers(session_id)}

def get_session_score(db: Session, current_user, session_id: str):
    session = _require_own_session(session_id, current_user.id)

    result = user_answer_service.calculate_score(session_id)

    quiz_id = int(session.get("quiz_id"))
    questions = question_crud.get_questions_by_quiz(db, quiz_id)
    max_score = sum(q.points for q in questions)

    db_result = result_crud.create_quiz_result(
        db=db, user_id=current_user.id, quiz_id=quiz_id,
        score=result["total_points"], max_score=max_score,
    )

    for answer in user_answer_service.get_all_answers(session_id):
        db.add(UserAnswer(
            quiz_result_id=db_result.id,
            question_id=int(answer.get("question_id")),
            answer_text=answer.get("answer_text"),
            answer_id=int(answer.get("answer_id")) if answer.get("answer_id") else None,
            is_correct=answer.get("is_correct") == "true",
            points_earned=int(answer.get("points_earned", 0)),
            time_spent_seconds=int(answer.get("time_spent_seconds", 0)),
        ))
    db.commit()

    _redis_sessions.delete_session(session_id)
    user_answer_service.delete_session_answers(session_id)

    return {
        "result_id": db_result.id,
        "total_points": result["total_points"],
        "total_questions": result["total_questions"],
        "correct_answers": result["correct_answers"],
        "percentage": result["percentage"],
        "max_score": max_score,
    }

def cancel_session(current_user, session_id: str):
    session = _redis_sessions.get_session(session_id)
    if session and int(session.get("user_id")) == current_user.id:
        _redis_sessions.delete_session(session_id)
        user_answer_service.delete_session_answers(session_id)
    return {"message": "Session cancelled"}
