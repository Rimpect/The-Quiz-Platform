import React from 'react'
import styles from '../Quiz.module.scss'

export const QuizLoading = () => {
  return (
    <div className={styles.loadingContainer}>
      <div className={styles.spinner}></div>
      <p>Загрузка вопросов...</p>
    </div>
  )
}
