import { Badge, getQuizDescriptionRoute, Button } from '@shared'
import { Eye, Check, X } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

import styles from './ViewQuizDialog.module.scss'

export function ViewQuizDialog({
  isOpen,
  quiz,
  onClose,
  onApprove,
  onRejectClick,
}) {
  const navigate = useNavigate()
  if (!isOpen || !quiz) return null

  const statusLabels = {
    approved: 'Одобрен',
    pending: 'На модерации',
    rejected: 'Отклонен',
  }

  return (
    <div className={styles.dialogOverlay} onClick={onClose}>
      <div
        className={styles.dialogContent}
        onClick={(e) => e.stopPropagation()}
      >
        <div className={styles.dialogHeader}>
          <h2 className={styles.dialogTitle}>Просмотр квиза</h2>
          <p className={styles.dialogDescription}>
            Детальная информация о квизе
          </p>
        </div>

        <div className={styles.dialogBody}>
          <div className={styles.viewQuizHeader}>
            <div>
              <h3 className={styles.viewQuizTitle}>{quiz.title}</h3>
              <Badge variant={quiz.status} size="sm">
                {statusLabels[quiz.status] || quiz.status}
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
                <p className={styles.detailValue}>{quiz.category}</p>
              </div>
              <div>
                <p className={styles.detailLabel}>Сложность</p>
                <p className={styles.detailValue}>{quiz.difficulty}</p>
              </div>
              <div>
                <p className={styles.detailLabel}>Вопросов</p>
                <p className={styles.detailValue}>{quiz.questionCount}</p>
              </div>
              <div>
                <p className={styles.detailLabel}>Дата создания</p>
                <p className={styles.detailValue}>{quiz.createdAt}</p>
              </div>
            </div>

            <div className={styles.descriptionBlock}>
              <p className={styles.detailLabel}>Описание</p>
              <p className={styles.descriptionText}>{quiz.description}</p>
            </div>
          </div>

          {quiz.status === 'pending' && (
            <div className={styles.viewActions}>
              <Button
                variant="green"
                fullWidth
                icon={<Check />} // или ✓
                onClick={() => onApprove(quiz)}
              >
                Одобрить
              </Button>

              <Button
                variant="red"
                fullWidth
                icon={<X />} // или ✗
                onClick={() => onRejectClick(quiz)}
              >
                Отклонить
              </Button>

              <Button
                variant="transparent"
                fullWidth
                icon={<Eye />}
                onClick={() => {
                  onClose()
                  navigate(getQuizDescriptionRoute(quiz.id))
                }}
              >
                Посмотреть
              </Button>
            </div>
          )}
        </div>

        <div className={styles.dialogFooter}>
          <Button variant="transparent" fullWidth onClick={onClose}>
            Закрыть
          </Button>
        </div>
      </div>
    </div>
  )
}
