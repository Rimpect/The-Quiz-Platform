from typing import Dict, Type, Union

from sqlalchemy.orm import Session

from ..models.model_achievement import UserAchievement


def get_user_achievements(db: Session, user_id: int) -> list[Type[UserAchievement]] :
    """Получение всех достижений пользователя"""
    return db.query(UserAchievement).filter(
        UserAchievement.user_id == user_id
    ).all()


def get_user_achievement_status(db: Session, user_id: int, achievement_id: int) -> bool :
    """Получение статуса конкретного достижения"""
    achievement = db.query(UserAchievement).filter(
        UserAchievement.user_id == user_id,
        UserAchievement.achievement_id == achievement_id
    ).first()

    if achievement :
        return achievement.is_unlocked
    return False


def unlock_achievement(db: Session, user_id: int, achievement_id: int) -> Union[Type[UserAchievement], UserAchievement] :
    """Разблокировка достижения для пользователя"""
    # Проверяем, существует ли запись
    existing = db.query(UserAchievement).filter(
        UserAchievement.user_id == user_id,
        UserAchievement.achievement_id == achievement_id
    ).first()

    if existing :
        if not existing.is_unlocked :
            existing.is_unlocked = True
            db.commit()
            db.refresh(existing)
        return existing

    # Создаём новую запись
    new_achievement = UserAchievement(
        user_id=user_id,
        achievement_id=achievement_id,
        is_unlocked=True
    )
    db.add(new_achievement)
    db.commit()
    db.refresh(new_achievement)
    return new_achievement


def create_achievement_record(db: Session, user_id: int, achievement_id: int) -> Union[Type[UserAchievement], UserAchievement] :
    """Создание записи о достижении (заблокированное)"""
    existing = db.query(UserAchievement).filter(
        UserAchievement.user_id == user_id,
        UserAchievement.achievement_id == achievement_id
    ).first()

    if existing :
        return existing

    new_achievement = UserAchievement(
        user_id=user_id,
        achievement_id=achievement_id,
        is_unlocked=False
    )
    db.add(new_achievement)
    db.commit()
    db.refresh(new_achievement)
    return new_achievement


def get_all_achievements_status(db: Session, user_id: int) -> Dict[int, bool] :
    """Получение статуса всех достижений пользователя"""
    achievements = get_user_achievements(db, user_id)
    return {a.achievement_id : a.is_unlocked for a in achievements}


def initialize_user_achievements(db: Session, user_id: int, total_achievements: int = 50) -> None :
    """Инициализация всех достижений для нового пользователя (все заблокированы)"""
    existing_count = db.query(UserAchievement).filter(
        UserAchievement.user_id == user_id
    ).count()

    if existing_count > 0 :
        return  # Уже инициализирован

    for ach_id in range(1, total_achievements + 1) :
        create_achievement_record(db, user_id, ach_id)