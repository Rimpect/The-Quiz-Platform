import { Eye } from 'lucide-react'

import styles from './QuizInfo.module.scss'

export function QuizInfo({ quiz, onApprove, onReject, onView }) {
  const getStatusBadge = (status) => {
    const variants = {
      approved: { label: 'Одобрен', className: styles.badgeApproved },
      pending: { label: 'На модерации', className: styles.badgePending },
      rejected: { label: 'Отклонен', className: styles.badgeRejected },
    }
    const variant = variants[status]
    return (
      <span className={`${styles.badge} ${variant.className}`}>
        {variant.label}
      </span>
    )
  }

  return (
    <div className={styles.quizCard}>
      <div className={styles.quizContent}>
        <div className={styles.quizInfo}>
          <div className={styles.quizHeader}>
            <h3 className={styles.quizTitle}>{quiz.title}</h3>
            {getStatusBadge(quiz.status)}
          </div>
          <p className={styles.quizDescription}>{quiz.description}</p>
          <div className={styles.quizMeta}>
            <span className={styles.metaItem}>👤 Автор: {quiz.author}</span>
            <span>•</span>
            <span className={styles.metaItem}>
              📁 Категория: {quiz.category}
            </span>
            <span>•</span>
            <span className={styles.metaItem}>
              ❓ Вопросов: {quiz.questionCount}
            </span>
            <span>•</span>
            <span className={styles.metaItem}>
              📊 Сложность: {quiz.difficulty}
            </span>
            <span>•</span>
            <span className={styles.metaItem}>📅 {quiz.createdAt}</span>
          </div>
        </div>

        <div className={styles.quizActions}>
          {quiz.status === 'pending' && (
            <>
              <button
                className={`${styles.actionButton} ${styles.approveButton}`}
                onClick={() => onApprove(quiz)}
              >
                ✓ Одобрить
              </button>
              <button
                className={`${styles.actionButton} ${styles.rejectButton}`}
                onClick={() => onReject(quiz)}
              >
                ✗ Отклонить
              </button>
            </>
          )}
          <button
            className={`${styles.actionButton} ${styles.viewButton}`}
            onClick={() => onView(quiz)}
          >
            <Eye size={20}></Eye> <span>Просмотр</span>
          </button>
        </div>
      </div>
    </div>
  )
}
