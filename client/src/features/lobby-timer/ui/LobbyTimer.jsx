import { useEffect, useState } from 'react'
import { Clock } from 'lucide-react'
import styles from './LobbyTimer.module.scss'

export function LobbyTimer({ initialTime, onTimeEnd, variant = 'default' }) {
  const [seconds, setSeconds] = useState(initialTime)

  const progressPercent = ((initialTime - seconds) / initialTime) * 100
  const remainingPercent = (seconds / initialTime) * 100

  const getProgressColor = (percent) => {
    if (percent > 50) return 'var(--color-green)'
    if (percent > 25) return 'var(--color-orange)'
    if (percent > 10) return 'var(--color-orange-red)'
    return 'var(--color-red)'
  }

  const progressColor = getProgressColor(remainingPercent)

  useEffect(() => {
    const interval = setInterval(() => {
      setSeconds((prev) => {
        if (prev <= 1) {
          clearInterval(interval)
          if (onTimeEnd) onTimeEnd()
          return 0
        }
        return prev - 1
      })
    }, 1000)

    return () => clearInterval(interval)
  }, [onTimeEnd])

  const minutes = Math.floor(seconds / 60)
  const secs = seconds % 60

  if (variant === 'default') {
    return (
      <div className={styles.timerContainer}>
        <div className={styles.timerText}>
          <Clock size={18} />
          Начало через
        </div>
        <div className={styles.timer} style={{ color: progressColor }}>
          {minutes}:{String(secs).padStart(2, '0')}
        </div>
        <div className={styles.progressBar}>
          <div
            className={styles.progressFill}
            style={{
              width: `${progressPercent}%`,
              background: progressColor,
            }}
          />
        </div>
      </div>
    )
  }

  if (variant === 'centered') {
    return (
      <div className={styles.timerCenteredContainer}>
        <div className={styles.timerCentered}>
          <div className={styles.timerTextCentered}>Начало через</div>
          <div
            className={styles.timerValueCentered}
            style={{ color: progressColor }}
          >
            {minutes}:{String(secs).padStart(2, '0')}
          </div>
        </div>
        <div className={styles.progressBarFull}>
          <div
            className={styles.progressFillFull}
            style={{
              width: `${progressPercent}%`,
              background: progressColor,
            }}
          />
        </div>
      </div>
    )
  }

  return null
}
