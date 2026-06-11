# from sqlalchemy import Column, Integer, Boolean, ForeignKey, UniqueConstraint
# from sqlalchemy.orm import relationship
# from ..database.database import Base
#
#
# class UserAchievement(Base):
#     """Таблица достижений пользователя"""
#     __tablename__ = "user_achievements"
#
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
#     achievement_id = Column(Integer, nullable=False, index=True)  # ID достижения (1, 2, 3...)
#     is_unlocked = Column(Boolean, default=False, nullable=False)  # Статус: получено/не получено
#
#     # Связь с пользователем
#     user = relationship("User", back_populates="achievements")
#
#     # Уникальная пара (user_id, achievement_id) - один пользователь не может иметь дубликатов
#     __table_args__ = (
#         UniqueConstraint('user_id', 'achievement_id', name='unique_user_achievement'),
#     )
#
#     def __repr__(self):
#         return f"<UserAchievement user_id={self.user_id}, achievement_id={self.achievement_id}, unlocked={self.is_unlocked}>"