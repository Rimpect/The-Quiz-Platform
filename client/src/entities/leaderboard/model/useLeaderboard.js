import { useEffect, useState } from 'react'

import { client } from '@shared/api/client'

export function useLeaderboard(quizId) {
  const [leaderboard, setLeaderboard] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!quizId) {
      setLeaderboard([])
      setLoading(false)
      return
    }

    setLoading(true)
    setError(null)

    client(`/quizzes/${quizId}/leaderboard`)
      .then((data) => {
        const items = Array.isArray(data) ? data : data?.items || []

        const mapped = items.map((item, idx) => ({
          place: item.place ?? idx + 1,
          name: item.name || 'Игрок',
          avatar: item.avatar || '/placeholder-avatar.png',
          percent: item.percent ?? 0,
          time: item.time || '0:00',
          score: item.score,
          maxScore: item.max_score,
          userId: item.user_id,
        }))

        setLeaderboard(mapped)
      })
      .catch((err) => {
        setError(err.message || 'Ошибка загрузки рейтинга')
        setLeaderboard([])
      })
      .finally(() => setLoading(false))
  }, [quizId])

  return { leaderboard, loading, error }
}
