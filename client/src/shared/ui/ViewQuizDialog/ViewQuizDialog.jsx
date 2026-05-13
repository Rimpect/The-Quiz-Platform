import styles from './ViewQuizDialog.module.scss'

export function ViewQuizDialog({
  isOpen,
  quiz,
  onClose,
  onApprove,
  onRejectClick,
}) {
  if (!isOpen || !quiz) return null

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
              {getStatusBadge(quiz.status)}
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
              <button
                className={`${styles.viewApproveButton} ${styles.viewButtonFull}`}
                onClick={() => onApprove(quiz)}
              >
                ✓ Одобрить
              </button>
              <button
                className={`${styles.viewRejectButton} ${styles.viewButtonFull}`}
                onClick={() => onRejectClick(quiz)}
              >
                ✗ Отклонить
              </button>
            </div>
          )}
        </div>

        <div className={styles.dialogFooter}>
          <button className={styles.closeButton} onClick={onClose}>
            Закрыть
          </button>
        </div>
      </div>
    </div>
  )
}
