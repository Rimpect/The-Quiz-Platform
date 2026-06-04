import { useEffect, useState } from 'react'

import { Clock } from 'lucide-react'

import styles from './LobbyTimer.module.scss'

export function LobbyTimer({ initialTime, onTimeEnd }) {
  const [seconds, setSeconds] = useState(initialTime)

  const progressPercent = ((initialTime - seconds) / initialTime) * 100

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

  return (
    <div className={styles.timerContainer}>
      <div className={styles.timerText}>
        <Clock size={18} color="red" />
        Начало через
      </div>
      <div className={styles.timer}>
        {minutes}:{String(secs).padStart(2, '0')}
      </div>
      <div className={styles.progressBar}>
        <div
          className={styles.progressFill}
          style={{ width: `${progressPercent}%` }}
        />
      </div>
    </div>
  )
}
