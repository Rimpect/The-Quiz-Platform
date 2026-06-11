import { useEffect } from 'react'

import styles from './WarningModal.module.scss'

export const WarningModal = ({ violations, remainingAttempts, onClose }) => {
  const getViolationMessage = (type) => {
    const messages = {
      tab_switch: 'Не переключайте вкладки во время прохождения квиза',
      copy_paste: 'Копирование и вставка запрещены',
      dev_tools: 'Инструменты разработчика отключены во время квиза',
    }
    return messages[type] || 'Обнаружено нарушение'
  }

  useEffect(() => {
    const timer = setTimeout(() => {
      if (onClose) onClose()
    }, 3000)

    return () => clearTimeout(timer)
  }, [onClose])

  return (
    <div className={styles.overlay}>
      <div className={styles.modal}>
        <div className={styles.warningIcon}>⚠️</div>
        <h3>Предупреждение!</h3>
        <div className={styles.violations}>
          {violations.map((v, i) => (
            <p key={i}>{getViolationMessage(v)}</p>
          ))}
        </div>
        {remainingAttempts !== undefined && (
          <p className={styles.remaining}>
            Осталось предупреждений: {remainingAttempts}
          </p>
        )}
      </div>
    </div>
  )
}
