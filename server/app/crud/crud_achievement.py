from typing import Dict, List, Type, Union

from sqlalchemy.orm import Session, joinedload

from ..models.model_achievement import UserAchievement

TOTAL_ACHIEVEMENTS = 10


def get_user_achievements(db: Session, user_id: int) -> list[Type[UserAchievement]]:
    return db.query(UserAchievement).filter(UserAchievement.user_id == user_id).all()


def get_all_achievements_status(db: Session, user_id: int) -> Dict[int, bool]:
    achievements = get_user_achievements(db, user_id)
    return {a.achievement_id: a.is_unlocked for a in achievements}


def unlock_achievement(
    db: Session, user_id: int, achievement_id: int
) -> Union[Type[UserAchievement], UserAchievement]:
    existing = db.query(UserAchievement).filter(
        UserAchievement.user_id == user_id,
        UserAchievement.achievement_id == achievement_id,
    ).first()

    if existing:
        if not existing.is_unlocked:
            existing.is_unlocked = True
            db.commit()
            db.refresh(existing)
        return existing

    new_ach = UserAchievement(user_id=user_id, achievement_id=achievement_id, is_unlocked=True)
    db.add(new_ach)
    db.commit()
    db.refresh(new_ach)
    return new_ach


def initialize_user_achievements(db: Session, user_id: int) -> None:
    existing_count = db.query(UserAchievement).filter(
        UserAchievement.user_id == user_id
    ).count()

    if existing_count > 0:
        return

    for ach_id in range(1, TOTAL_ACHIEVEMENTS + 1):
        db.add(UserAchievement(user_id=user_id, achievement_id=ach_id, is_unlocked=False))
    db.commit()


def check_and_unlock_achievements(db: Session, user_id: int) -> List[int]:
    """
    Проверяет условия всех достижений и разблокирует выполненные.
    Возвращает список ID только что разблокированных достижений.
    """
    from ..models.model_quiz_result import QuizResult

    # Загружаем все завершённые результаты с данными квиза
    results = (
        db.query(QuizResult)
        .options(joinedload(QuizResult.quiz))
        .filter(QuizResult.user_id == user_id, QuizResult.is_completed == True)
        .all()
    )

    total_completed = len(results)

    perfect_scores = sum(
        1 for r in results
        if r.max_score > 0 and (r.score / r.max_score) * 100 >= 99.9
    )

    categories_covered = {
        r.quiz.category_id
        for r in results
        if r.quiz and r.quiz.category_id is not None
    }

    has_fast_quiz = any(
        0 < r.duration_seconds < 60 for r in results
    )

    has_high_score = any(
        r.max_score > 0 and (r.score / r.max_score) * 100 >= 90
        for r in results
    )

    # Условия в порядке ID достижений из achievementsList.js:
    # 1  🏆 Первый квиз        — пройти 1 квиз
    # 2  🎯 Снайпер            — хотя бы 1 результат с 100%
    # 3  ⚡ Быстрый ум         — 10 квизов
    # 4  🔥 Горячая серия      — 5 квизов
    # 5  📚 Эрудит             — 50 квизов
    # 6  💎 Перфекционист      — 10 результатов с 100%
    # 7  🎓 Ученик             — квизы минимум в 3 разных категориях
    # 8  🚀 Ракета             — закончить квиз менее чем за 60 секунд
    # 9  🏅 Чемпион            — хотя бы 1 результат ≥ 90%
    # 10 💪 Упорный            — 100 квизов
    conditions = {
        1: total_completed >= 1,
        2: perfect_scores >= 1,
        3: total_completed >= 10,
        4: total_completed >= 5,
        5: total_completed >= 50,
        6: perfect_scores >= 10,
        7: len(categories_covered) >= 3,
        8: has_fast_quiz,
        9: has_high_score,
        10: total_completed >= 100,
    }

    current_status = get_all_achievements_status(db, user_id)
    newly_unlocked = []

    for ach_id, condition_met in conditions.items():
        if condition_met and not current_status.get(ach_id, False):
            unlock_achievement(db, user_id, ach_id)
            newly_unlocked.append(ach_id)

    return newly_unlocked
