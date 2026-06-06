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
      <div className={styles.imageWrapper}>
        <img src={img} alt={title} className={styles.image} />
        <div className={styles.badgeContainer}>
          <Badge variant={badgeVariant} size="sm">
            {difficulty}
          </Badge>
        </div>
      </div>

      <div className={styles.content}>
        <div className={styles.category}>
          <Trophy className={styles.categoryIcon} />
          <span>{category}</span>
        </div>

        <h3 className={styles.title}>{title}</h3>
        <p className={styles.description}>{description}</p>

        <div className={styles.info}>
          <div className={styles.infoItem}>
            <Users size={16} />
            <span>{participants}</span>
          </div>
          <div className={styles.infoItem}>
            <Clock size={16} />
            <span>{duration} мин</span>
          </div>
        </div>
      </div>
    </article>
  )
}
