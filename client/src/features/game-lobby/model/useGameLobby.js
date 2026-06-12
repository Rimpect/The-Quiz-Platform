import { useEffect, useRef, useState, useCallback } from 'react'

import { useUser } from '@entities'
import { client } from '@shared/api/client'
import { toast } from 'sonner'

const POLL_INTERVAL_MS = 1000

/**
 * Реальная синхронизация лобби через HTTP-поллинг общей игровой сессии.
 * Все игроки одного квиза попадают в одну сессию (find-or-create на сервере),
 * затем периодически опрашивают её состояние.
 *
 * @param {number|string} quizId
 * @param {'competitive'|'team'} gameMode
 */
export function useGameLobby(quizId, gameMode) {
  const currentUser = useUser()
  const [sessionId, setSessionId] = useState(null)
  const [players, setPlayers] = useState([])
  const [teams, setTeams] = useState([])
  const [lobbyStarted, setLobbyStarted] = useState(false)
  const [lobbyTimeLeft, setLobbyTimeLeft] = useState(null)
  const [loading, setLoading] = useState(true)
  const pollRef = useRef(null)

  const applyState = useCallback((state) => {
    if (!state) return
    setPlayers(Array.isArray(state.players) ? state.players : [])
    setTeams(Array.isArray(state.teams) ? state.teams : [])
    setLobbyStarted(!!state.lobby_started)
    if (typeof state.lobby_time_left === 'number') {
      setLobbyTimeLeft(state.lobby_time_left)
    }
  }, [])

  // Вход в общее лобби при монтировании
  useEffect(() => {
    if (!quizId || !gameMode) return

    let cancelled = false

    const joinLobby = async () => {
      try {
        const state = await client('/game/lobby/join', {
          method: 'POST',
          body: JSON.stringify({
            quiz_id: Number(quizId),
            game_mode: gameMode,
          }),
        })
        if (cancelled) return
        setSessionId(state.session_id)
        applyState(state)
      } catch (err) {
        if (!cancelled) toast.error(err.message || 'Не удалось войти в лобби')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    joinLobby()

    return () => {
      cancelled = true
    }
  }, [quizId, gameMode, applyState])

  // Поллинг состояния сессии
  useEffect(() => {
    if (!sessionId) return

    const poll = async () => {
      try {
        const state = await client(`/game/sessions/${sessionId}`)
        applyState(state)
      } catch {
        // Сессия могла истечь — тихо игнорируем единичные ошибки поллинга
      }
    }

    pollRef.current = setInterval(poll, POLL_INTERVAL_MS)
    return () => clearInterval(pollRef.current)
  }, [sessionId, applyState])

  const markReady = useCallback(async () => {
    if (!sessionId) return
    try {
      const state = await client(`/game/sessions/${sessionId}/ready`, {
        method: 'POST',
      })
      applyState(state)
    } catch (err) {
      toast.error(err.message || 'Ошибка')
    }
  }, [sessionId, applyState])

  // Форс-старт по истечении таймера лобби
  const startLobby = useCallback(async () => {
    if (!sessionId) return
    try {
      const state = await client(`/game/sessions/${sessionId}/start`, {
        method: 'POST',
      })
      applyState(state)
    } catch (err) {
      toast.error(err.message || 'Ошибка старта')
    }
  }, [sessionId, applyState])

  const createTeam = useCallback(
    async (teamName) => {
      if (!sessionId) return
      try {
        const res = await client(`/game/sessions/${sessionId}/teams/create`, {
          method: 'POST',
          body: JSON.stringify({ team_name: teamName }),
        })
        applyState(res?.state)
        toast.success(`Команда "${teamName}" создана`)
      } catch (err) {
        toast.error(err.message || 'Ошибка создания команды')
      }
    },
    [sessionId, applyState],
  )

  const joinTeam = useCallback(
    async (teamId) => {
      if (!sessionId) return
      try {
        const state = await client(`/game/sessions/${sessionId}/teams/join`, {
          method: 'POST',
          body: JSON.stringify({ team_id: teamId }),
        })
        applyState(state)
      } catch (err) {
        toast.error(err.message || 'Ошибка присоединения к команде')
      }
    },
    [sessionId, applyState],
  )

  const leaveTeam = useCallback(async () => {
    if (!sessionId) return
    try {
      const state = await client(`/game/sessions/${sessionId}/teams/leave`, {
        method: 'POST',
      })
      applyState(state)
    } catch (err) {
      toast.error(err.message || 'Ошибка')
    }
  }, [sessionId, applyState])

  const myId = currentUser?.id
  const me = players.find((p) => p.user_id === myId)
  const myReady = !!me?.is_ready
  const myTeamId = me?.team_id || null
  const readyCount = players.filter((p) => p.is_ready).length

  return {
    sessionId,
    players,
    teams,
    lobbyStarted,
    lobbyTimeLeft,
    loading,
    myReady,
    myTeamId,
    readyCount,
    markReady,
    startLobby,
    createTeam,
    joinTeam,
    leaveTeam,
  }
}
