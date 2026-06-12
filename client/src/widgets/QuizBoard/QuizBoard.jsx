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

  const { paginatedQuizList, totalPages, activePage, filteredQuizList } =
    useQuizBoard(quizzes, currentPage)

  return (
    <div className={styles.containerBoard}>
      {loading && <div className={styles.statusMsg}>Загрузка квизов...</div>}
      {error && <div className={styles.statusMsg}>{error}</div>}
      {!loading && !error && filteredQuizList.length === 0 && (
        <div className={styles.statusMsg}>Квизы не найдены.</div>
      )}

      {!loading && !error && paginatedQuizList.length > 0 && (
        <div className={styles.dashboardQuiz}>
          {paginatedQuizList.map((quiz) => (
            <Link key={quiz.id} to={getQuizDescriptionRoute(quiz.id)}>
              <QuizCard {...quiz} />
            </Link>
          ))}
        </div>
      )}

      {open && (
        <ModalNotifications open={open} onClose={() => setOpen(false)}>
          буковки
        </ModalNotifications>
      )}

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
