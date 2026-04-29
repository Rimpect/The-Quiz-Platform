import { useState } from 'react'

import styles from './RejectQuizDialog.module.scss'

export function RejectQuizDialog({ isOpen, quiz, onClose, onConfirm }) {
  const [reason, setReason] = useState('')

  if (!isOpen || !quiz) return null

  const handleConfirm = () => {
    if (!reason.trim()) {
      alert('Укажите причину отклонения')
      return
    }
    onConfirm(reason)
    setReason('')
  }

  return (
    <div className={styles.dialogOverlay} onClick={onClose}>
      <div
        className={styles.dialogContent}
        onClick={(e) => e.stopPropagation()}
      >
        <div className={styles.dialogHeader}>
          <h2 className={styles.dialogTitle}>Отклонить квиз</h2>
          <p className={styles.dialogDescription}>
            Укажите причину отклонения квиза "{quiz.title}". Автор увидит это
            сообщение.
          </p>
        </div>

        <div className={styles.dialogBody}>
          <textarea
            className={styles.rejectTextarea}
            placeholder="Например: Недостаточно уникальных вопросов, содержимое не соответствует теме..."
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            rows={4}
          />
        </div>

        <div className={styles.dialogFooter}>
          <button className={styles.cancelButton} onClick={onClose}>
            Отмена
          </button>
          <button
            className={styles.confirmRejectButton}
            onClick={handleConfirm}
          >
            Отклонить квиз
          </button>
        </div>
      </div>
    </div>
  )
}
