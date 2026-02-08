import React from "react";
import "./QuizCard";
export function QuizCard(props) {
    const {img}=props
  // картинка, описание и тд будут сделаны через пропсы
  return (
    <div>
      <div className="quiz-card">
        <img src={img} alt="" className="quiz-card__image" />
        <div className="quiz-card__content">
          <p className="quiz-card__description">Краткое описание</p>
          <div className="quiz-card__complexity">
            <span className="quiz-card__complexity-label">Сложность:</span>
            <div className="quiz-card__complexity-icons">
              {/* иконки сложности */}
            </div>
          </div>
        </div>
        <button className="quiz-card__button button">Кнопка</button>
      </div>
    </div>
  );
}
