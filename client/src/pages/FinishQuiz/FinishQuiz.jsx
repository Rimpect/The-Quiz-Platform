import React from "react";
import { useLocation, useParams, useNavigate } from "react-router-dom";
export function FinishQuiz() {
  const location = useLocation();
  const { id } = useParams();
  const navigate = useNavigate();
  const {
    totalScore = 0,
    maxPossibleScore = 100,
    percentScore = 0,
    correctCount = 0,
    totalQuestions = 0,
  } = location.state || {};

  const goToHome = () => {
    navigate("/");
  };
  const retakeQuiz = () => {
    navigate(`/QuizPage/:id`);
    // ${id}
  };

  return (
    <div class="finish">
      <div class="finish__header">
        <h2 class="finish__title finish__title--icon">Иконка кубка</h2>
        <h2 class="finish__title finish__title--encouragement">
          Не сдавайтесь! 💪
        </h2>
        <div class="finish__subtitle">Квиз #{id} завершен</div>
      </div>

      <div class="finish__results">
        <div class="finish__score-circle">
          <span class="finish__score-percent">{percentScore}%</span>
        </div>

        <div class="finish__score-details">
          <h3 class="finish__details-title">Ваш результат:</h3>g
          <p class="finish__score-text">
            {totalScore} из {maxPossibleScore} баллов
          </p>
          <p class="finish__correct-count">
            Правильных ответов: {correctCount} из {totalQuestions}
          </p>
        </div>
      </div>

      <div class="finish__actions">
        <button
          class="finish__button finish__button--primary"
          onClick={goToHome}
        >
          Вернуться на главную
        </button>
        <button
          class="finish__button finish__button--secondary"
          onClick={retakeQuiz}
        >
          Пройти еще раз
        </button>
      </div>

      <div class="finish__message">
        Каждая попытка делает вас умнее! Попробуйте пройти квиз снова или
        выберите другой.
      </div>
    </div>
  );
}
export default FinishQuiz;
