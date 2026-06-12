import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'

import { RulesGate } from '@features'
import { LobbyTeams, LobbyRating } from '@widgets'
import { client } from '@shared/api/client'

export function LobbyTeamsPage() {
  const { quizId } = useParams()
  const navigate = useNavigate()
  const [quiz, setQuiz] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!quizId) {
      setLoading(false)
      return
    }

    setLoading(true)
    client(`/quizzes/${quizId}`)
      .then((data) => {
        // Если это competitive, перенаправляем на лобби рейтингового режима
        if (data.quiz_mode === 'competitive') {
          navigate(`/lobbyRating/${quizId}`)
          return
        }

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
      .catch(() => {
        setQuiz({
          id: quizId,
          title: 'Квиз',
          questionCount: 0,
          duration: 0,
          difficulty: 'Легкий',
        })
      })
      .finally(() => setLoading(false))
  }, [quizId, navigate])

  if (loading) {
    return <div style={{ padding: '2rem', textAlign: 'center' }}>Загрузка...</div>
  }

  if (!quiz) return null

  return (
    <RulesGate quizId={quizId}>
      <LobbyTeams quiz={quiz} quizId={quizId} />
    </RulesGate>
  )
}
