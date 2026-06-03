import { Badge } from '@shared'
import { Users, Clock, Trophy } from 'lucide-react'

import styles from './QuizCard.module.scss'

export function QuizCard(props) {
  const {
    img,
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

  const badgeVariant = difficultyMap[difficulty] || 'easy'

  return (
    <article className={styles.card}>
      <div className={styles.card__imageWrapper}>
        <img src={img} alt={title} className={styles.card__image} />
        <Badge variant={badgeVariant} size="sm">
          {difficulty}
        </Badge>
      </div>

      <div className={styles.card__content}>
        <div className={styles.card__category}>
          <span className={styles.card__categoryIcon}>
            <Trophy className={styles.card__categoryIconSvg} />
          </span>
          <span className={styles.card__categoryText}>{category}</span>
        </div>

        <h3 className={styles.card__title}>{title}</h3>
        <p className={styles.card__description}>{description}</p>

        <div className={styles.card__info}>
          <div className={styles.card__infoItem}>
            <span className={styles.card__infoItemIcon}>
              <Users />
            </span>
            <span className={styles.card__infoItemText}>{participants}</span>
          </div>
          <div className={styles.card__infoItem}>
            <span className={styles.card__infoItemIcon}>
              <Clock />
            </span>
            <span className={styles.card__infoItemText}>{duration} мин</span>
          </div>
        </div>
      </div>
    </article>
  )
}
