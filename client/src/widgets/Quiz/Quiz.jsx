import React, { useEffect, useState } from 'react'

import { AntiCheatProvider } from '@features/anti-cheating'
import { client } from '@shared/api/client'
import { useNavigate, useParams, useLocation } from 'react-router-dom'

import { QuizContent } from './QuizContent'
import { SyncedQuizContent } from './SyncedQuizContent'

const SESSION_TTL_MS = 3 * 60 * 60 * 1000 // 3 часа — как TTL сессии на сервере

export function Quiz() {
  const { id } = useParams()
  const navigate = useNavigate()
  const location = useLocation()
  const [loading, setLoading] = useState(true)

  const storageKey = `quizSession:${id}`

  // Сессия из лобби; при перезагрузке вкладки (моб. сворачивание) location.state
  // теряется — восстанавливаем sessionId из sessionStorage, чтобы не выпасть из
  // synced-сессии (иначе серверный бан/состояние не применятся).
  const [sessionId] = useState(() => {
    if (location.state?.sessionId) return location.state.sessionId
    try {
      const raw = sessionStorage.getItem(storageKey)
      if (raw) {
        const { sessionId: sid, ts } = JSON.parse(raw)
        if (sid && Date.now() - ts < SESSION_TTL_MS) return sid
      }
    } catch {
      // повреждённое значение — игнорируем
    }
    return null
  })

  // Запоминаем сессию для переживания перезагрузки
  useEffect(() => {
    if (location.state?.sessionId) {
      sessionStorage.setItem(
        storageKey,
        JSON.stringify({ sessionId: location.state.sessionId, ts: Date.now() }),
      )
    }
  }, [storageKey, location.state])

  // Проверяем режим квиза ПЕРЕД рендерингом
  useEffect(() => {
    // Сессия известна (из лобби или восстановлена) → сразу synced, без редиректа
    if (!id || location.state?.fromLobby || sessionId) {
      setLoading(false)
      return
    }

    const checkQuizMode = async () => {
      try {
        const response = await client(`/quizzes/${id}`)
        const quizData = response?.data ?? response

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
  }, [id, navigate, location.state, sessionId])

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
