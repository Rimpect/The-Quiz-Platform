from ..database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Boolean, Text

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
    