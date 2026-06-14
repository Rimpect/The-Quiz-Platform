import { Badge, getDifficulty, QUIZ_MODE_LABELS } from '@shared'
import { Users, Clock, Trophy } from 'lucide-react'

import styles from './QuizCard.module.scss'

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
  const { variant: badgeVariant, label: difficultyLabel } =
    getDifficulty(difficulty)
  const showModeBadge =
    quiz_mode && quiz_mode !== 'single' && quiz_mode !== 'solo'

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
      </div>

      <div className={styles.content}>
        <div className={styles.category}>
          <Trophy className={styles.categoryIcon} />
          <span>{category || 'Без категории'}</span>
        </div>

        <h3 className={styles.title}>{title}</h3>
        <p className={styles.description}>{description}</p>

        {/* Бейджи в контенте — всегда читаемы (не зависят от фона обложки) */}
        <div className={styles.badges}>
          <Badge variant={badgeVariant} size="sm">
            {difficultyLabel}
          </Badge>
          {showModeBadge && (
            <Badge variant={quiz_mode} size="sm">
              {QUIZ_MODE_LABELS[quiz_mode] || quiz_mode}
            </Badge>
          )}
        </div>

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
