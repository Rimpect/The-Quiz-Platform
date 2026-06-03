import React, { useMemo, useState } from 'react'

import { useQuizzes } from '@entities/quiz'
import { useSearchStore } from '@features/search-quiz/model/search.store'
import { useQuizSearch } from '@features/search-quiz/model/useQuizSearch'
import { Pagination, QuizCard, ModalNotifications, createRoute } from '@shared'
import { Link } from 'react-router-dom'

import styles from './QuizeBoard.module.scss'

export function QuizeBoard({ currentPage, onPageChange, totalPages }) {
  const [open, setOpen] = useState(false)
  const { quizzes, loading, error } = useQuizzes()
  const query = useSearchStore((state) => state.query)
  const filter = useSearchStore((state) => state.filter)

  const quizList = Array.isArray(quizzes) ? quizzes : []

  const filteredQuizList = useMemo(() => {
    const searchedQuizzes = query.trim()
      ? useQuizSearch(quizList, query)
      : quizList

    return searchedQuizzes.filter((quiz) => {
      if (
        filter.categories?.length > 0 &&
        !filter.categories.includes(quiz.category)
      ) {
        return false
      }

      if (filter.difficulty && quiz.difficulty !== filter.difficulty) {
        return false
      }

      if (
        filter.typeQuestions?.length > 0 &&
        quiz.typeQuestions &&
        !filter.typeQuestions.includes(quiz.typeQuestions)
      ) {
        return false
      }

      if (
        filter.mediaType?.length > 0 &&
        quiz.mediaType &&
        !filter.mediaType.includes(quiz.mediaType)
      ) {
        return false
      }

      if (
        filter.numberOfQuestionsFrom != null &&
        typeof quiz.questionCount === 'number' &&
        quiz.questionCount < filter.numberOfQuestionsFrom
      ) {
        return false
      }

      if (
        filter.numberOfQuestionsTo != null &&
        typeof quiz.questionCount === 'number' &&
        quiz.questionCount > filter.numberOfQuestionsTo
      ) {
        return false
      }

      if (
        filter.durationFrom != null &&
        typeof quiz.duration === 'number' &&
        quiz.duration < filter.durationFrom
      ) {
        return false
      }

      if (
        filter.durationTo != null &&
        typeof quiz.duration === 'number' &&
        quiz.duration > filter.durationTo
      ) {
        return false
      }

      if (filter.typeQuiz && quiz.typeQuiz !== filter.typeQuiz) {
        return false
      }

      return true
    })
  }, [quizList, query, filter])

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
          filteredQuizList.map((quiz) => (
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
