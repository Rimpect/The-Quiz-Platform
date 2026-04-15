import React from 'react'

import './QuizCard.scss'
import { Users, Clock, Trophy } from 'lucide-react'

export function QuizCard(props) {
  const {
    img,
    id,
    description,
    difficulty,
    title,
    category,
    participants,
    duration,
  } = props
  const difficultyMap = {
    Легкий: 'easy',
    Средний: 'medium',
    Сложный: 'hard',
  }
  const badgeClass = difficultyMap[difficulty] || 'easy'
  return (
    <div className="quiz-card">
      <div className="quiz-card__image-wrapper">
        <img
          src={img}
          alt={`${title} - квиз ${id}`}
          className="quiz-card__image"
        />
        <span className={`quiz-card__badge quiz-card__badge--${badgeClass}`}>
          {difficulty}
        </span>
      </div>

      <div className="quiz-card__content">
        <div className="quiz-card__category">
          <span className="quiz-card__category-icon">
            <Trophy className="quiz-card__category-icon-svg" />
          </span>
          <span className="quiz-card__category-text">{category}</span>
        </div>

        <h3 className="quiz-card__title">{title}</h3>
        <p className="quiz-card__description">{description}</p>

        <div className="quiz-card__info">
          <div className="quiz-card__info-item">
            <span className="quiz-card__info-icon">
              <Users />
            </span>
            <span className="quiz-card__info-text">{participants}</span>
          </div>
          <div className="quiz-card__info-item">
            <span className="quiz-card__info-icon">
              <Clock />
            </span>
            <span className="quiz-card__info-text">{duration} мин</span>
          </div>
        </div>
      </div>
    </div>
  )
}
