import React, { useState } from 'react'

import { useQuizzes } from '@entities/quiz'
import { useQuizBoard } from '@features/quiz-board'
import {
  Pagination,
  QuizCard,
  ModalNotifications,
  getQuizDescriptionRoute,
} from '@shared'
import { Link } from 'react-router-dom'

import styles from './QuizBoard.module.scss'

export function QuizBoard({ currentPage, onPageChange }) {
  const [open, setOpen] = useState(false)
  const { quizzes, loading, error } = useQuizzes()

  const quizList = Array.isArray(quizzes) ? quizzes : []
  const { paginatedQuizList, totalPages, activePage, filteredQuizList } =
    useQuizBoard(quizList, currentPage)

  return (
    <div className={styles.containerBoard}>
      <div className={styles.dashboardQuiz}>
        {loading && <div>Загрузка квизов...</div>}
        {error && <div className={styles.error}>{error}</div>}
        {!loading && !error && filteredQuizList.length === 0 && (
          <div>Квизы не найдены.</div>
        )}
        {!loading &&
          !error &&
          paginatedQuizList.map((quiz) => (
            <Link key={quiz.id} to={getQuizDescriptionRoute(quiz.id)}>
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
        currentPage={activePage}
        totalPages={totalPages}
        onPageChange={onPageChange}
      />
    </div>
  )
}
