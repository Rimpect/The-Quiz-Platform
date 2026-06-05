from sqlalchemy import Column, Integer, ForeignKey, Boolean
from ..database.database import Base


class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True, index=True)
    quiz_result_id = Column(Integer, ForeignKey("quiz_results.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)

    # Ответ пользователя
    answer_id = Column(Integer, ForeignKey("answers.id"), nullable=True)  # Для выбранного варианта
    is_correct = Column(Boolean, default=False, nullable=False)
    points_earned = Column(Integer, default=0, nullable=False)

    time_spent_seconds = Column(Integer, nullable=True)  # Время затраченное на вопрос

    def __repr__(self):
        return f"<UserAnswer = {self.user_answer_id}, quiz={self.quiz_id}, score={self.score}>"
