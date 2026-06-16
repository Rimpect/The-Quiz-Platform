import { useCallback, useEffect, useState } from 'react'

import { client } from '@shared/api/client'

const formatDate = (iso) => {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('ru-RU')
}

const mapQuiz = (q, status) => ({
  id: q.id,
  title: q.title,
  status: q.status || status,
  category: q.category_obj?.category_type || q.category || '',
  difficulty: q.difficulty || 'easy',
  participants: q.times_taken || 0,
  total_questions: q.total_questions || 0,
  createdAt: formatDate(q.created_at),
  created_at: q.created_at,
  rejectionReason: q.rejection_reason || '',
})

export function useMyQuizzes() {
  const [myQuizzes, setMyQuizzes] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchQuizzes = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await client('/users/me/quizzes')

      const approved = (data?.approved || []).map((q) => mapQuiz(q, 'approved'))
      const pending = (data?.pending || []).map((q) => mapQuiz(q, 'pending'))
      const rejected = (data?.rejected || []).map((q) => mapQuiz(q, 'rejected'))

      setMyQuizzes([...pending, ...approved, ...rejected])
    } catch {
      setError('Не удалось загрузить квизы')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchQuizzes()
  }, [fetchQuizzes])

  const deleteQuiz = useCallback(
    async (quizId) => {
      await client(`/users/me/quizzes/${quizId}`, { method: 'DELETE' })
      await fetchQuizzes()
    },
    [fetchQuizzes],
  )

  return { myQuizzes, loading, error, deleteQuiz, refetch: fetchQuizzes }
}
