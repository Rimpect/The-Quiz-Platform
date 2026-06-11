import { useTimer } from '../model/useTimer'

import styles from './QuizTimer.module.scss'

export function QuizTimer({ duration, onTimeEnd }) {
  const { timeLeft, isWarning } = useTimer({
    duration,
    onTimeEnd,
    enableSound: true,
    isLobby: false,
  })

  return (
    <div className={`${styles.timer} ${isWarning ? styles.warning : ''}`}>
      <span className={styles.timerLabel}>Осталось времени:</span>
      <span className={styles.timerValue}>{timeLeft} сек</span>
    </div>
  )
}
