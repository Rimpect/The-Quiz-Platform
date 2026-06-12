import { useEffect, useState } from 'react'

import { client } from '@shared/api/client'

const formatDuration = (seconds) => {
  if (!seconds) return '—'
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return m > 0 ? `${m}м ${s}с` : `${s}с`
}

const formatDate = (iso) => {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('ru-RU')
}

export function useQuizHistory() {
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    let canceled = false

    const fetch = async () => {
      setLoading(true)
      try {
        const data = await client('/quiz-results/me/history')
        if (canceled) return
        const list = Array.isArray(data) ? data : []
        setHistory(
          list.map((r) => ({
            id: r.id,
            title: r.title,
            category: r.category || '',
            score: Math.round(r.percentage || 0),
            correctAnswers: Math.round(r.score || 0),
            totalQuestions: r.total_questions || 0,
            time: formatDuration(r.duration_seconds),
            date: formatDate(r.completed_at),
          })),
        )
      } catch {
        if (!canceled) setError('Не удалось загрузить историю')
      } finally {
        if (!canceled) setLoading(false)
      }
    }

    fetch()
    return () => {
      canceled = true
    }
  }, [])

  return { history, loading, error }
}
