import React, { useEffect, useState } from 'react'

import { AntiCheatProvider } from '@features/anti-cheating'
import { client } from '@shared/api/client'
import { useNavigate, useParams, useLocation } from 'react-router-dom'

import { QuizContent } from './QuizContent'
import { SyncedQuizContent } from './SyncedQuizContent'

export function Quiz() {
  const { id } = useParams()
  const navigate = useNavigate()
  const location = useLocation()
  const [loading, setLoading] = useState(true)

  // Сессия из лобби → синхронизированное прохождение (командный/рейтинговый)
  const sessionId = location.state?.sessionId || null

  // Проверяем режим квиза ПЕРЕД рендерингом
  useEffect(() => {
    if (!id || location.state?.fromLobby) {
      setLoading(false)
      return
    }

    const checkQuizMode = async () => {
      try {
        const response = await client(`/quizzes/${id}`)
        const quizData = response?.data ?? response

        // Только командный режим идёт через лобби (хост-сессия).
        // Рейтинговый — асинхронный: играется как соло, результат в общий лидерборд.
        if (quizData.quiz_mode === 'team') {
          navigate(`/quiz/${id}/lobby`)
          return
        }
      } catch (err) {
        console.error('Error checking quiz mode:', err)
      } finally {
        setLoading(false)
      }
    }

    checkQuizMode()
  }, [id, navigate, location.state])

  const handleDecline = () => {
    navigate(-1)
  }

  if (loading) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center' }}>Загрузка...</div>
    )
  }

  return (
    <AntiCheatProvider
      quizId={id}
      onDecline={handleDecline}
      config={{
        maxWarnings: 3,
        autoSubmitOnViolation: false,
        blockCopyPaste: true,
        blockDevTools: true,
      }}
    >
      {sessionId ? (
        <SyncedQuizContent quizId={id} sessionId={sessionId} />
      ) : (
        <QuizContent quizId={id} />
      )}
    </AntiCheatProvider>
  )
}
