import { useEffect, useState } from 'react'

import { client } from '@shared/api/client'

export function useProfileStats() {
  const [stats, setStats] = useState({
    totalQuizzes: 0,
    averageScore: 0,
    bestResult: 0,
    totalMinutes: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    client('/users/me/statistics')
      .then((data) => {
        if (data) {
          setStats({
            totalQuizzes: data.total_quizzes_completed ?? 0,
            averageScore: data.average_score ?? 0,
            bestResult: data.best_result ?? 0,
            totalMinutes: data.total_minutes ?? 0,
          })
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  return { stats, loading }
}
