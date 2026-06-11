import { request } from '@shared'

// export const getQuestions = (quizId) => request(`/quizzes/${quizId}/questions`)

// export const getQuestionById = (quizId, questionId) =>
//   request(`/quizzes/${quizId}/questions/${questionId}`)

// export const getQuestions = (quizId) => request(`/questions?quizId=${quizId}`)

export const getQuestions = (quizId) => {
  if (quizId) {
    return request(`/questions?quizId=${quizId}`) // БЕЗ кавычек!
  }
  return request('/questions')
}
