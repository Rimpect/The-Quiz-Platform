"""
Роутер для управления сессиями прохождения квизов
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..crud import crud_quiz as quiz_crud
from ..crud import crud_question as question_crud
from ..crud import crud_user_answer as answer_service
from ..database.database import get_db
from ..utils.security import get_current_user, get_current_guest
from ..config_redis.redis_service import QuizSessionService
from .. import schemas, models

router = APIRouter(prefix="/quiz-session", tags=["quiz-sessions"])

# Сервисы
quiz_session_service = QuizSessionService()


@router.post("/start", response_model=schemas.StartSessionResponse)
def start_session(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
) :
    """Начало новой сессии прохождения квиза"""
    # Проверяем существование квиза
    quiz = quiz_crud.get_quiz(db, quiz_id)
    if not quiz :
        raise HTTPException(status_code=404, detail="Quiz not found")

    # Получаем вопросы
    questions = question_crud.get_questions_by_quiz(db, quiz_id)

    # Создаем сессию в Redis
    session_id = quiz_session_service.create_session(
        user_id=current_user.id,
        quiz_id=quiz_id,
        total_questions=len(questions)
    )

    return schemas.StartSessionResponse(
        session_id=session_id,
        quiz_id=quiz_id,
        total_questions=len(questions),
        expires_in_minutes=60
    )


@router.post("/guest/start", response_model=schemas.StartSessionResponse)
def start_guest_session(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_guest: models.Guest = Depends(get_current_guest)
) :
    """Начало сессии для гостя"""
    quiz = quiz_crud.get_quiz(db, quiz_id)
    if not quiz :
        raise HTTPException(status_code=404, detail="Quiz not found")

    if not quiz.is_public :
        raise HTTPException(status_code=403, detail="Guests can only play public quizzes")

    questions = question_crud.get_questions_by_quiz(db, quiz_id)

    # Для гостя используем guest_id как user_id (отрицательное число)
    session_id = quiz_session_service.create_session(
        user_id=-current_guest.id,  # Отрицательное значение для гостей
        quiz_id=quiz_id,
        total_questions=len(questions)
    )

    return schemas.StartSessionResponse(
        session_id=session_id,
        quiz_id=quiz_id,
        total_questions=len(questions),
        expires_in_minutes=60
    )


@router.post("/answer")
def save_answer(
        session_id: str,
        answer: schemas.UserAnswerCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
) :
    """Сохранение ответа пользователя"""
    # Проверяем сессию
    session = quiz_session_service.get_session(session_id)
    if not session :
        raise HTTPException(status_code=404, detail="Session not found")

    if int(session.get("user_id")) != current_user.id :
        raise HTTPException(status_code=403, detail="Not your session")

    # Получаем вопрос
    question = question_crud.get_question(db, answer.question_id)
    if not question :
        raise HTTPException(status_code=404, detail="Question not found")

    # Сохраняем ответ
    result = answer_service.UserAnswerService.save_answer(
        session_id=session_id,
        user_id=current_user.id,
        quiz_id=int(session.get("quiz_id")),
        question_id=answer.question_id,
        answer_data=answer
    )

    return {
        "message" : "Answer saved",
        "is_correct" : result["is_correct"],
        "points_earned" : result["points_earned"]
    }


@router.get("/answers")
def get_session_answers(
        session_id: str,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
) :
    """Получение всех ответов сессии"""
    session = quiz_session_service.get_session(session_id)
    if not session :
        raise HTTPException(status_code=404, detail="Session not found")

    if int(session.get("user_id")) != current_user.id :
        raise HTTPException(status_code=403, detail="Not your session")

    answers = answer_service.UserAnswerService.get_all_answers(session_id)
    return {"answers" : answers}


@router.get("/score")
def get_session_score(
        session_id: str,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
) :
    """Подсчет результатов и завершение сессии"""
    session = quiz_session_service.get_session(session_id)
    if not session :
        raise HTTPException(status_code=404, detail="Session not found")

    if int(session.get("user_id")) != current_user.id :
        raise HTTPException(status_code=403, detail="Not your session")

    # Подсчитываем результат
    result = answer_service.UserAnswerService.calculate_score(session_id)

    # Сохраняем результат в БД
    from ..crud import crud_quiz_result as result_crud
    db_result = result_crud.create_quiz_result(
        db=db,
        user_id=current_user.id,
        quiz_id=int(session.get("quiz_id")),
        score=result["total_points"],
        max_score=result["total_questions"] * 10
    )

    # Удаляем сессию из Redis
    quiz_session_service.delete_session(session_id)
    answer_service.UserAnswerService.delete_session_answers(session_id)

    return result


@router.delete("/{session_id}")
def cancel_session(
        session_id: str,
        current_user: models.User = Depends(get_current_user)
) :
    """Отмена сессии (удаление временных данных)"""
    session = quiz_session_service.get_session(session_id)
    if session and int(session.get("user_id")) == current_user.id :
        quiz_session_service.delete_session(session_id)
        answer_service.UserAnswerService.delete_session_answers(session_id)

    return {"message" : "Session cancelled"}