import { request } from '@shared'

export const getQuizzes = () => request('/quizzes')
export const getQuizById = (id) => request(`/quizzes/${id}`)
export const getQuizFull = (id) => request(`/quizzes/${id}/full`)
export const createQuiz = (data) =>
  request('/quizzes', {
    method: 'POST',
    body: JSON.stringify(data),
  })
export const updateQuiz = (id, data) =>
  request(`/quizzes/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  })
export const deleteQuiz = (id) =>
  request(`/quizzes/${id}`, {
    method: 'DELETE',
  })
export const getCategories = () => request('/quizzes/categories')
export const getLeaderboard = (id) => request(`/quizzes/${id}/leaderboard`)
