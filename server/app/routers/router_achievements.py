# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
#
# from ..crud import crud_achievement as achievement_crud
# from ..database.database import get_db
# from ..models.model_user import User
# from ..schemas.schemas_response import ResponseFactory
# from ..utils.security import get_current_user
#
# router = APIRouter(prefix="/achievements", tags=["achievements"])
#
#
# @router.get("/")
# def get_my_achievements(
#         db: Session = Depends(get_db),
#         current_user: User = Depends(get_current_user)
# ) :
#     """Получение статуса всех достижений текущего пользователя"""
#     achievements = achievement_crud.get_user_achievements(db, current_user.id)
#
#     # Формируем ответ: {achievement_id: is_unlocked}
#     result = {
#         "user_id" : current_user.id,
#         "achievements" : {
#             str(a.achievement_id) : a.is_unlocked for a in achievements
#         }
#     }
#
#     return ResponseFactory.success(
#         data=result,
#         message="Achievements retrieved successfully"
#     )
#
#
# @router.get("/{achievement_id}")
# def get_achievement_status(
#         achievement_id: int,
#         db: Session = Depends(get_db),
#         current_user: User = Depends(get_current_user)
# ) :
#     """Получение статуса конкретного достижения"""
#     is_unlocked = achievement_crud.get_user_achievement_status(
#         db, current_user.id, achievement_id
#     )
#
#     return ResponseFactory.success(
#         data={
#             "achievement_id" : achievement_id,
#             "is_unlocked" : is_unlocked
#         },
#         message="Achievement status retrieved"
#     )
#
#
# @router.post("/{achievement_id}/unlock")
# def unlock_achievement(
#         achievement_id: int,
#         db: Session = Depends(get_db),
#         current_user: User = Depends(get_current_user)
# ) :
#     """Разблокировка достижения (вызывается при выполнении условия)"""
#     achievement = achievement_crud.unlock_achievement(db, current_user.id, achievement_id)
#
#     return ResponseFactory.success(
#         data={
#             "achievement_id" : achievement.achievement_id,
#             "is_unlocked" : achievement.is_unlocked
#         },
#         message="Achievement unlocked successfully"
#     )