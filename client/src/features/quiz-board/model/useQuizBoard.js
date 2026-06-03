import { useMemo } from 'react'

import { useSearchStore } from '@features/search-quiz/model/search.store'
import { useQuizSearch } from '@features/search-quiz/model/useQuizSearch'

const DEFAULT_ITEMS_PER_PAGE = 12

const matchesQuizFilter = (quiz, filter) => {
  if (!filter) {
    return true
  }

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
}

export function useQuizBoard(
  quizzes = [],
  currentPage = 1,
  itemsPerPage = DEFAULT_ITEMS_PER_PAGE,
) {
  const query = useSearchStore((state) => state.query)
  const filter = useSearchStore((state) => state.filter)

  return useMemo(() => {
    const quizList = Array.isArray(quizzes) ? quizzes : []
    const searchedQuizzes = query.trim()
      ? useQuizSearch(quizList, query)
      : quizList

    const filteredQuizList = searchedQuizzes.filter((quiz) =>
      matchesQuizFilter(quiz, filter),
    )

    const pages = Math.max(1, Math.ceil(filteredQuizList.length / itemsPerPage))
    const activePage = Math.max(1, Math.min(Number(currentPage) || 1, pages))

    const startIndex = (activePage - 1) * itemsPerPage
    const paginatedQuizList = filteredQuizList.slice(
      startIndex,
      startIndex + itemsPerPage,
    )

    return {
      paginatedQuizList,
      filteredQuizList,
      totalPages: pages,
      activePage,
    }
  }, [quizzes, query, filter, currentPage, itemsPerPage])
}
