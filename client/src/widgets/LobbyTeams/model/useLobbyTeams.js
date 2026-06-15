import { useEffect, useRef } from 'react'

import { useTimerSound } from '@features'
import { useGameLobby } from '@features/game-lobby'
import { ROUTES } from '@shared'
import { useNavigate } from 'react-router-dom'
import { toast } from 'sonner'

export function useLobbyTeams(quizId) {
  const navigate = useNavigate()
  const startedRef = useRef(false)
  const leftRef = useRef(false)

  const lobby = useGameLobby(quizId, 'team')
  const { sessionId, lobbyStarted, lobbyTimeLeft, cancelled, leaveLobby, createTeam } =
    lobby

  useTimerSound(lobbyTimeLeft)

  useEffect(() => {
    if (lobbyStarted && !startedRef.current) {
      startedRef.current = true
      toast.success('Все готовы! Начинаем квиз...')
      navigate(`/quiz/${quizId}`, { state: { fromLobby: true, sessionId } })
    }
  }, [lobbyStarted, quizId, navigate, sessionId])

  useEffect(() => {
    if (cancelled && !leftRef.current && !startedRef.current) {
      leftRef.current = true
      toast.error('Хост покинул лобби — оно закрыто')
      navigate(ROUTES.main, { replace: true })
    }
  }, [cancelled, navigate])

  const handleLeave = async () => {
    leftRef.current = true
    await leaveLobby()
    navigate(ROUTES.main, { replace: true })
  }

  const handleCreateTeam = (newTeam) => createTeam(newTeam.name)

  return { ...lobby, handleLeave, handleCreateTeam }
}
