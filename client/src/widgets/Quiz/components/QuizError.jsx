import React from 'react'
import { Link } from 'react-router-dom'
import { ROUTES } from '@shared'
import styles from '../Quiz.module.scss'

export const QuizError = ({ error }) => {
  return (
    <div className={styles.errorContainer}>
      <h2>Ошибка</h2>
      <p>{error}</p>
      <Link to={ROUTES.main} className={styles.backButton}>
        Вернуться на главную
      </Link>
    </div>
  )
}
