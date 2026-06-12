import { useEffect } from 'react'

import { Button } from '../Button'

import styles from './ConfirmDialog.module.scss'

/**
 * Переиспользуемая модалка подтверждения (удаление и т.п.).
 */
export function ConfirmDialog({
  isOpen,
  title = 'Подтвердите действие',
  message,
  confirmText = 'Удалить',
  cancelText = 'Отмена',
  onConfirm,
  onCancel,
  loading = false,
}) {
  useEffect(() => {
    if (!isOpen) return
    const prev = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => {
      document.body.style.overflow = prev
    }
  }, [isOpen])

  if (!isOpen) return null

  return (
    <div className={styles.overlay} onClick={onCancel}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <h3 className={styles.title}>{title}</h3>
        {message && <p className={styles.message}>{message}</p>}

        <div className={styles.actions}>
          <Button variant="white" onClick={onCancel} disabled={loading}>
            {cancelText}
          </Button>
          <Button variant="red" onClick={onConfirm} disabled={loading}>
            {loading ? 'Удаление...' : confirmText}
          </Button>
        </div>
      </div>
    </div>
  )
}
