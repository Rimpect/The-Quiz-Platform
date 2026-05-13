import { Button } from '@shared'
import { Eye, Dot, Users, Check, X } from 'lucide-react'

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
            <span className={styles.metaItem}>
              <Users /> Автор: {quiz.author}
            </span>
            <Dot />
            <span className={styles.metaItem}>Категория: {quiz.category}</span>
            <Dot />
            <span className={styles.metaItem}>
              Вопросов: {quiz.questionCount}
            </span>
            <Dot />
            <span className={styles.metaItem}>
              Сложность: {quiz.difficulty}
            </span>
            <Dot />
            <span className={styles.metaItem}> {quiz.createdAt}</span>
          </div>
        </div>

        <div className={styles.quizActions}>
          {quiz.status === 'pending' && (
            <>
              <Button
                variant="green"
                size="medium"
                icon={<Check size={20} />}
                onClick={() => onApprove(quiz)}
              >
                Одобрить
              </Button>
              <Button
                variant="red"
                size="medium"
                icon={<X size={20} />}
                onClick={() => onReject(quiz)}
              >
                Отклонить
              </Button>
            </>
          )}
          <Button
            variant="white"
            size="medium"
            icon={<Eye size={20} />}
            onClick={() => onView(quiz)}
          >
            Просмотр
          </Button>
        </div>
      </div>
    </div>
  )
}
