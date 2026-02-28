import React from "react";
import "./QuizCard.scss";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrophy, faUsers, faClock } from "@fortawesome/free-solid-svg-icons";
export function QuizCard(props) {
  const { img, id, description, difficulty } = props;

  return (
    <div className="quiz-card">
      <div className="quiz-card__inner">
        <div className="quiz-card__image-wrapper">
          <img src={img} alt={`Квиз ${id}`} className="quiz-card__image" />
          <span className={`quiz-card__badge quiz-card__badge--${difficulty}`}>
            Сложность
          </span>
        </div>
        <div className="quiz-card__content">
          <div className="quiz-card__category">
            <div className="quiz-card__category-icon">
              {" "}
              <FontAwesomeIcon
                icon={faTrophy}
                className="quiz-card__category-icon-svg"
              />
            </div>
            <div className="quiz-card__category-text">
              текст к какой категории относится квиз
            </div>
          </div>
          <div className="quiz-card__title">Title</div>
          <p className="quiz-card__description">
            {description} Lorem ipsum dolor sit amet consectetur adipisicing
            elit. Asperiores architecto nobis veniam sint accusantium! Quis modi
            et, dicta blanditiis animi earum, molestias pariatur nesciunt in
            nobis necessitatibus quos placeat beatae.
          </p>

          {/* Блок сложности */}
          <div className="quiz-card__info">
            <div className="quiz-card__info-item">
              <FontAwesomeIcon
                icon={faUsers}
                className="quiz-card__info-icon-svg"
              />
              <span className="quiz-card__info-text">128</span>
            </div>
            <div className="quiz-card__info-item">
              <FontAwesomeIcon
                icon={faClock}
                className="quiz-card__info-icon-svg"
              />
              <span className="quiz-card__info-text">15 мин</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
