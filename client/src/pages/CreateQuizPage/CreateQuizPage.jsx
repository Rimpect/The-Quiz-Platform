import React, { useEffect, useRef } from 'react'

import { QuizStats, QuizQuestions } from '@features'
import { useQuizStore } from '@features/quiz-editor'
import { client } from '@shared/api/client'
import { HeaderCreateQuiz } from '@widgets'
import { useLocation } from 'react-router-dom'

import styles from './CreateQuizPage.module.scss'

export function CreateQuizPage() {
  const location = useLocation()
  const loadQuiz = useQuizStore((state) => state.loadQuiz)
  const resetQuiz = useQuizStore((state) => state.resetQuiz)
  const editQuizId = location.state?.editQuizId
  const loaded = useRef(false)

  useEffect(() => {
    if (!editQuizId) {
      resetQuiz()
      return
    }
    if (loaded.current) return
    loaded.current = true

    client(`/quizzes/${editQuizId}/edit`)
      .then((data) => {
        if (data) loadQuiz(data)
      })
      .catch(() => {})
  }, [editQuizId])

  return (
    <div className={styles.main}>
      <HeaderCreateQuiz />
      <div className={styles.container}>
        <div className={styles.label}>
          {editQuizId ? 'Редактировать квиз' : 'Создать новый квиз'}
        </div>
        <div>
          <QuizStats />
          <div className={styles.questions} />
          <QuizQuestions />
        </div>
      </div>
    </div>
  )
}
