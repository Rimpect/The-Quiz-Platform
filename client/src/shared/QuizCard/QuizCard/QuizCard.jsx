import React from "react";
import "./QuizCard.scss";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSignal } from "@fortawesome/free-solid-svg-icons";
export function QuizCard(props) {
  const { img, id, description } = props;

  return (
    <div className="quiz-card">
      <button className="quiz-card__button button">
        <div className="quiz-card__image-wrapper">
          <img src={img} alt={`Квиз ${id}`} className="quiz-card__image" />
        </div>
        <div className="quiz-card__content">
          <p className="quiz-card__description">
            {description} Lorem ipsum dolor sit amet consectetur adipisicing
            elit. Asperiores architecto nobis veniam sint accusantium! Quis modi
            et, dicta blanditiis animi earum, molestias pariatur nesciunt in
            nobis necessitatibus quos placeat beatae.
          </p>

          {/* Блок сложности */}
          <div className="quiz-card__complexity">
            <span className="quiz-card__complexity-label">Сложность:</span>
            <div className="quiz-card__complexity-icons">
              {/* Иконки сложности - пример */}
              <span className="quiz-card__complexity-icon quiz-card__complexity-icon--active">Легкая</span>
              <FontAwesomeIcon
                icon={faSignal}
                className="quiz-card__complexity-icon"
              />
            </div>
          </div>
        </div>
      </button>
    </div>
  );
}
