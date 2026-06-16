import { useCallback, useEffect, useState } from 'react'

import {
  getPendingQuizzes,
  getApprovedQuizzes,
  getRejectedQuizzes,
  approveQuiz,
  rejectQuiz,
} from '../api/adminApi'

export function useAdminQuizzes() {
  const [pending, setPending] = useState([])
  const [approved, setApproved] = useState([])
  const [rejected, setRejected] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchAll = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const [p, a, r] = await Promise.all([
        getPendingQuizzes(),
        getApprovedQuizzes(),
        getRejectedQuizzes(),
      ])
      setPending(Array.isArray(p) ? p : [])
      setApproved(Array.isArray(a) ? a : [])
      setRejected(Array.isArray(r) ? r : [])
    } catch (e) {
      setError(e.message || 'Ошибка загрузки')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchAll()
  }, [fetchAll])

  const handleApprove = useCallback(
    async (quiz) => {
      await approveQuiz(quiz.id)
      await fetchAll()
    },
    [fetchAll],
  )

  const handleReject = useCallback(
    async (quiz, reason) => {
      await rejectQuiz(quiz.id, reason)
      await fetchAll()
    },
    [fetchAll],
  )

  const allQuizzes = [
    ...pending.map((q) => ({ ...q, status: 'pending' })),
    ...approved.map((q) => ({ ...q, status: 'approved' })),
    ...rejected.map((q) => ({ ...q, status: 'rejected' })),
  ]

  return {
    pending,
    approved,
    rejected,
    allQuizzes,
    loading,
    error,
    handleApprove,
    handleReject,
    refetch: fetchAll,
    fetchAll,
  }
}
