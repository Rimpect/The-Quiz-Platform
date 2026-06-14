import { useTimer } from '../model/useTimer'

import styles from './QuizTimer.module.scss'

export function QuizTimer({ duration, onTimeEnd, timeLeft: external }) {
  // Управляемый режим: время приходит снаружи (серверное, synced-квизы).
  // Иначе — собственный локальный отсчёт со звуком (соло-квиз).
  const isControlled = external !== undefined
  const internal = useTimer({
    duration: duration ?? 0,
    onTimeEnd: isControlled ? undefined : onTimeEnd,
    enableSound: !isControlled,
    isLobby: false,
  })

  const timeLeft = isControlled ? external : internal.timeLeft
  const isWarning = isControlled
    ? timeLeft != null && timeLeft <= 10 && timeLeft > 0
    : internal.isWarning

  return (
    <div className={`${styles.timer} ${isWarning ? styles.warning : ''}`}>
      <span className={styles.timerLabel}>Осталось времени:</span>
      <span className={styles.timerValue}>
        {timeLeft != null ? `${timeLeft} сек` : '—'}
      </span>
    </div>
  )
}
