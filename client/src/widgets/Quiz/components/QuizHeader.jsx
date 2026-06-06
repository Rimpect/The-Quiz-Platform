import React from 'react'
import { Link } from 'react-router-dom'
import { QuizTimer } from '@features'
import { ROUTES } from '@shared'
import styles from '../Quiz.module.scss'

export const QuizHeader = ({ title, category, onTimeEnd, timerKey }) => {
  return (
    <div className={styles.quizHeader}>
      <div className={styles.quizInfo}>
        <Link to={ROUTES.main} className={styles.exitLink}>
          Выход
        </Link>
        <div className={styles.quizTitle}>{title || 'Квиз'}</div>
        <div className={styles.quizCategory}>{category || 'Общий'}</div>
      </div>
      <QuizTimer key={timerKey} duration={30} onTimeEnd={onTimeEnd} />
    </div>
  )
}
