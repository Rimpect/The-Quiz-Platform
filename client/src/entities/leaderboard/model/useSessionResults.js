import { useEffect, useState } from 'react'

import { client } from '@shared/api/client'

/**
 * Результаты по конкретной игровой сессии — только та группа, что играла вместе.
 * Отличается от useLeaderboard (глобальный рейтинг по квизу за всё время).
 */
export function useSessionResults(sessionId) {
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!sessionId) {
      setResults([])
      setLoading(false)
      return
    }

    setLoading(true)
    setError(null)

    client(`/game/sessions/${sessionId}/results`)
      .then((data) => {
        const items = Array.isArray(data) ? data : []
        setResults(
          items.map((item, idx) => ({
            place: item.place ?? idx + 1,
            name: item.name || 'Игрок',
            avatar: item.is_team
              ? null
              : item.avatar || '/placeholder-avatar.png',
            isTeam: !!item.is_team,
            percent: item.percent ?? 0,
            time: item.time || '0:00',
            score: item.score,
            maxScore: item.max_score,
            correct: item.correct,
            members: item.members,
            teamName: item.team_name,
            userId: item.user_id,
          })),
        )
      })
      .catch((err) => {
        setError(err.message || 'Ошибка загрузки результатов')
        setResults([])
      })
      .finally(() => setLoading(false))
  }, [sessionId])

  return { results, loading, error }
}
