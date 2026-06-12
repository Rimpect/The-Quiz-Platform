import { client } from '@shared/api/client'

export const createQuizResult = (quizId) =>
  client('/quiz-results', {
    method: 'POST',
    body: JSON.stringify({ quiz_id: quizId }),
  })

export const getMyResults = () => client('/quiz-results/me')

export const getResultById = (id) => client(`/quiz-results/${id}`)

export const completeQuiz = (resultId) =>
  client(`/quiz-results/${resultId}/complete`, { method: 'POST' })

export const getQuizLeaderboard = (quizId) =>
  client(`/quiz-results/quiz/${quizId}/leaderboard`)
