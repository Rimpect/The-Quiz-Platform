import { useQuizTimer } from '../model/useQuizTimer'

import styles from './QuizTimer.module.scss'

export function QuizTimer({ duration, onTimeEnd, warningSound }) {
  const { timeLeft, isWarning } = useQuizTimer({
    duration,
    onTimeEnd,
    warningSound,
  })

  return (
    <div className={`${styles.timer} ${isWarning ? styles.warning : ''}`}>
      <span className={styles.timerLabel}>Осталось времени:</span>

      <span className={styles.timerValue}>{timeLeft} сек</span>
    </div>
  )
}
