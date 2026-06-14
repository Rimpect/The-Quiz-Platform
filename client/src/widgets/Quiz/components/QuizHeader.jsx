import React from 'react'

import { QuizTimer } from '@features'
import { ROUTES } from '@shared'
import { Link } from 'react-router-dom'

import styles from '../Quiz.module.scss'

export const QuizHeader = ({
  title,
  timerKey,
  onTimeEnd,
  timeLimitSeconds,
}) => {
  return (
    <div className={styles.quizHeader}>
      <div className={styles.quizInfo}>
        <Link to={ROUTES.main} className={styles.exitLink}>
          Выход
        </Link>
        <div className={styles.quizTitle}>{title || 'Квиз'}</div>
      </div>
      {timeLimitSeconds > 0 && (
        <QuizTimer
          key={timerKey}
          duration={timeLimitSeconds}
          onTimeEnd={onTimeEnd}
        />
      )}
    </div>
  )
}
