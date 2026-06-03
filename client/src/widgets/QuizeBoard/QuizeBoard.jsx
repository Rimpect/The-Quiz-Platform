import React, { useState } from 'react'

import { useQuizzes } from '@entities/quiz'
import { Pagination, QuizCard, ModalNotifications, createRoute } from '@shared'

import { Link } from 'react-router-dom'
import styles from './QuizeBoard.module.scss'

export function QuizeBoard({ currentPage, onPageChange, totalPages }) {
  const [open, setOpen] = useState(false)
  const { quizzes, loading, error } = useQuizzes()

  const quizList = Array.isArray(quizzes) ? quizzes : []

  return (
    <div className={styles.containerBoard}>
      <div className={styles.dashboardQuiz}>
        {loading && <div>Загрузка квизов...</div>}
        {error && <div className={styles.error}>{error}</div>}
        {!loading && !error && quizList.length === 0 && (
          <div>Квизы не найдены.</div>
        )}
        {!loading &&
          !error &&
          quizList.map((quiz) => (
            <Link key={quiz.id} to={createRoute.quizDescription(quiz.id)}>
              <QuizCard {...quiz} />
            </Link>
          ))}

        {open && (
          <ModalNotifications open={open} onClose={() => setOpen(false)}>
            буковки
          </ModalNotifications>
        )}
      </div>
      <Pagination
        variant="main"
        pageInfo="hidden"
        currentPage={currentPage}
        totalPages={totalPages}
        onPageChange={onPageChange}
      />
    </div>
  )
}
