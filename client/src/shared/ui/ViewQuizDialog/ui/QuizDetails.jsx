import { Badge } from '@shared'

import styles from '../ViewQuizDialog.module.scss'

const STATUS_LABELS = {
  approved: 'Одобрен',
  pending: 'На модерации',
  rejected: 'Отклонен',
}

const DIFFICULTY_LABELS = {
  easy: 'Лёгкий',
  medium: 'Средний',
  hard: 'Сложный',
}

/** Заголовок, сетка характеристик и описание квиза. */
export function QuizDetails({ quiz }) {
  return (
    <>
      <div className={styles.viewQuizHeader}>
        <div>
          <h3 className={styles.viewQuizTitle}>{quiz.title}</h3>
          <Badge variant={quiz.status} size="sm">
            {STATUS_LABELS[quiz.status] || quiz.status}
          </Badge>
        </div>
      </div>

      <div className={styles.viewQuizDetails}>
        <div className={styles.detailsGrid}>
          <div>
            <p className={styles.detailLabel}>Автор</p>
            <p className={styles.detailValue}>{quiz.author}</p>
          </div>
          <div>
            <p className={styles.detailLabel}>Категория</p>
            <p className={styles.detailValue}>{quiz.category || 'Нет'}</p>
          </div>
          <div>
            <p className={styles.detailLabel}>Сложность</p>
            <p className={styles.detailValue}>
              {DIFFICULTY_LABELS[quiz.difficulty] || quiz.difficulty}
            </p>
          </div>
          <div>
            <p className={styles.detailLabel}>Вопросов</p>
            <p className={styles.detailValue}>{quiz.total_questions || 0}</p>
          </div>
          <div>
            <p className={styles.detailLabel}>Длительность</p>
            <p className={styles.detailValue}>
              {quiz.duration_minutes
                ? `${quiz.duration_minutes} мин`
                : 'без лимита'}
            </p>
          </div>
          <div>
            <p className={styles.detailLabel}>Тип</p>
            <p className={styles.detailValue}>{quiz.quiz_mode || 'одиночный'}</p>
          </div>
        </div>

        <div className={styles.descriptionBlock}>
          <p className={styles.detailLabel}>Описание</p>
          <p className={styles.descriptionText}>{quiz.description}</p>
        </div>
      </div>
    </>
  )
}
