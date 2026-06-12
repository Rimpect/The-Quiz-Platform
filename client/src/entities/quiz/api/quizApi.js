import { client } from '@shared/api/client'

// Преобразует серверный формат квиза в клиентский (QuizCard ожидает эти поля)
const normalizeQuiz = (quiz) => ({
  ...quiz,
  img: quiz.cover_url || null,
  category: quiz.category_obj?.category_type || quiz.category || '',
  difficulty: quiz.difficulty || 'easy',
  participants: quiz.times_taken || 0,
  duration: quiz.duration_minutes || 0,
  questionCount: quiz.total_questions || 0,
  mediaTypes: quiz.media_types || [],
  author: quiz.author_name || null,
})

export const getQuizzes = async () => {
  const data = await client('/quizzes')
  const list = Array.isArray(data) ? data : []
  return list.map(normalizeQuiz)
}

export const getQuizById = async (id) => {
  const data = await client(`/quizzes/${id}`)
  return data ? normalizeQuiz(data) : data
}

export const getQuizFull = (id) => client(`/quizzes/${id}/full`)

export const createQuiz = (data) =>
  client('/quizzes', { method: 'POST', body: JSON.stringify(data) })

export const updateQuiz = (id, data) =>
  client(`/quizzes/${id}`, { method: 'PUT', body: JSON.stringify(data) })

export const deleteQuiz = (id) => client(`/quizzes/${id}`, { method: 'DELETE' })

export const getCategories = () => client('/quizzes/categories')

export const getLeaderboard = (id) => client(`/quizzes/${id}/leaderboard`)
