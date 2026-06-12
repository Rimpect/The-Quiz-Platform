import { client } from '@shared/api/client'

export const getPendingQuizzes = () => client('/admin/pending')
export const getApprovedQuizzes = () => client('/admin/quizzes')
export const getRejectedQuizzes = () => client('/admin/rejected')

export const approveQuiz = (id) =>
  client(`/admin/quizzes/${id}/approve`, { method: 'POST' })

export const rejectQuiz = (id) =>
  client(`/admin/quizzes/${id}/reject`, { method: 'POST' })

export const deleteAdminQuiz = (id) =>
  client(`/admin/quizzes/${id}`, { method: 'DELETE' })
