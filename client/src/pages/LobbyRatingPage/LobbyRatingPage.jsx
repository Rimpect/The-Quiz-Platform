import { useEffect, useState } from 'react'

import { RulesGate } from '@features'
import { client } from '@shared/api/client'
import { LobbyRating } from '@widgets'
import { useParams } from 'react-router-dom'

export function LobbyRatingPage() {
  const { id } = useParams()
  const [quiz, setQuiz] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!id) return

    setLoading(true)
    client(`/quizzes/${id}`)
      .then((data) => {
        setQuiz({
          id: data.id,
          title: data.title,
          questionCount: data.total_questions || 0,
          duration: data.duration_minutes || 0,
          difficulty: data.difficulty || 'Легкий',
          description: data.description,
          quiz_mode: data.quiz_mode,
          lobby_wait_time_seconds: data.lobby_wait_time_seconds || 30,
        })
      })
      .catch(() => setQuiz(null))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return <div style={{ padding: '2rem', textAlign: 'center' }}>Загрузка...</div>

  // Лобби ожидания для рейтингового (competitive) квиза.
  // Правила принимаются ДО входа в лобби через RulesGate.
  return (
    <RulesGate quizId={id}>
      <LobbyRating quiz={quiz || {}} quizId={id} />
    </RulesGate>
  )
}
