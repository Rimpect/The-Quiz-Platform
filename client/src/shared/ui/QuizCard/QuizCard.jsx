import { Badge } from '@shared'
import { Users, Clock, Trophy } from 'lucide-react'

import styles from './QuizCard.module.scss'

const DIFFICULTY_LABELS = {
  easy: 'Лёгкий',
  medium: 'Средний',
  hard: 'Сложный',
}

const QUIZ_MODE_LABELS = {
  single: 'Соло',
  team: 'Командный',
  competitive: 'Рейтинговый',
}

const DEFAULT_COVER = '/placeholder-quiz.png'

export function QuizCard(props) {
  const {
    cover_url,
    img,
    description,
    difficulty,
    title,
    category,
    participants,
    duration,
    quiz_mode,
  } = props

  const coverSrc = cover_url || img || DEFAULT_COVER
  const difficultyLabel =
    DIFFICULTY_LABELS[difficulty] || difficulty || 'Лёгкий'
  const badgeVariant = difficulty || 'easy'

  return (
    <article className={styles.card}>
      <div className={styles.imageWrapper}>
        <img
          src={coverSrc}
          alt={title}
          className={styles.image}
          onError={(e) => {
            e.currentTarget.src = DEFAULT_COVER
          }}
        />
        <div className={styles.badgeContainer}>
          <Badge variant={badgeVariant} size="sm">
            {difficultyLabel}
          </Badge>
          {quiz_mode && quiz_mode !== 'single' && (
            <Badge variant={quiz_mode} size="sm">
              {QUIZ_MODE_LABELS[quiz_mode] || quiz_mode}
            </Badge>
          )}
        </div>
      </div>

      <div className={styles.content}>
        <div className={styles.category}>
          <Trophy className={styles.categoryIcon} />
          <span>{category || 'Без категории'}</span>
        </div>

        <h3 className={styles.title}>{title}</h3>
        <p className={styles.description}>{description}</p>

        <div className={styles.info}>
          <div className={styles.infoItem}>
            <Users size={16} />
            <span>{participants ?? 0}</span>
          </div>
          <div className={styles.infoItem}>
            <Clock size={16} />
            <span>{duration ? `${duration} мин` : 'без лимита'}</span>
          </div>
        </div>
      </div>
    </article>
  )
}
