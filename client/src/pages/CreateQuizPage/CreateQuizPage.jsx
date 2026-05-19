import React from 'react'

import { QuizStats, HeaderCreateQuiz, QuizQuestion } from '@widgets'

import styles from './CreateQuizPage.module.scss'

export function CreateQuizPage() {
  return (
    <div className={styles.main}>
      <HeaderCreateQuiz></HeaderCreateQuiz>
      <div className={styles.container}>
        <div className={styles.label}>Создать новый квиз</div>
        <div>
          <QuizStats></QuizStats>
          <div className={styles.questions}></div>
          <QuizQuestion></QuizQuestion>
        </div>
      </div>
    </div>
  )
}
