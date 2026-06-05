from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..database.database import Base


class Category(Base):
    """Справочник категорий квизов"""
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    category_type = Column(String(100), unique=True, nullable=False, index=True)

    # Связь с квизами (один ко многим)
    quizzes = relationship("Quiz", back_populates="category_ref")

    def __repr__(self):
        return f"<Category {self.category_type}>"
