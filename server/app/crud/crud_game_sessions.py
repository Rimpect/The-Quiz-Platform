"""
CRUD операции для игровых сессий и результатов
"""
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional, List

from ..models.model_game_session import GameSession, GameMode, TeamMember
from ..models.model_user_answer import UserAnswer
from ..models.model_quiz_result import QuizResult


def create_game_session(
    db: Session,
    session_id: str,
    quiz_id: int,
    game_mode: str,
    team_id: Optional[str] = None,
    team_name: Optional[str] = None,
) -> GameSession:
    """Создать запись игровой сессии в БД"""
    db_session = GameSession(
        session_id=session_id,
        quiz_id=quiz_id,
        game_mode=game_mode,
        team_id=team_id,
        team_name=team_name,
        started_at=datetime.utcnow(),
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def add_team_member(
    db: Session,
    session_id: str,
    team_id: str,
    user_id: int,
) -> TeamMember:
    """Добавить участника команды"""
    member = TeamMember(
        session_id=session_id,
        team_id=team_id,
        user_id=user_id,
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


def save_user_answer(
    db: Session,
    session_id: str,
    user_id: int,
    quiz_id: int,
    question_id: int,
    answer_ids: List[int],
    is_correct: bool,
    points_earned: int,
    time_spent_seconds: int,
    question_order: int,
) -> UserAnswer:
    """Сохранить ответ пользователя"""
    import json

    user_answer = UserAnswer(
        session_id=session_id,
        user_id=user_id,
        quiz_id=quiz_id,
        question_id=question_id,
        answer_ids=json.dumps(answer_ids),
        is_correct=is_correct,
        points_earned=points_earned,
        time_spent_seconds=time_spent_seconds,
        question_order=question_order,
        completed_at=datetime.utcnow(),
    )
    db.add(user_answer)
    db.commit()
    db.refresh(user_answer)
    return user_answer


def save_quiz_result(
    db: Session,
    user_id: int,
    quiz_id: int,
    score: float,
    max_score: float,
    is_completed: bool = True,
) -> QuizResult:
    """Сохранить итоговый результат прохождения квиза"""
    result = QuizResult(
        user_id=user_id,
        quiz_id=quiz_id,
        score=score,
        max_score=max_score,
        is_completed=is_completed,
        completed_at=datetime.utcnow(),
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def get_game_session(db: Session, session_id: str) -> Optional[GameSession]:
    """Получить сессию"""
    return db.query(GameSession).filter(GameSession.session_id == session_id).first()


def get_session_answers(db: Session, session_id: str) -> List[UserAnswer]:
    """Получить все ответы в сессии"""
    return db.query(UserAnswer).filter(UserAnswer.session_id == session_id).all()


def get_team_members(db: Session, session_id: str, team_id: str) -> List[TeamMember]:
    """Получить членов команды"""
    return db.query(TeamMember).filter(
        TeamMember.session_id == session_id,
        TeamMember.team_id == team_id
    ).all()


def end_game_session(db: Session, session_id: str) -> GameSession:
    """Завершить игровую сессию"""
    session = get_game_session(db, session_id)
    if session:
        session.ended_at = datetime.utcnow()
        db.commit()
        db.refresh(session)
    return session
