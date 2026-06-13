import { useCallback, useEffect, useRef, useState } from 'react'

import { useQuestions, useQuestionStore, useUser } from '@entities'
import {
  calculatePartialScore,
  useAnswerSelection,
  checkAnswer,
} from '@features'
import { useGameSocket } from '@features/game-lobby/model/useGameSocket'
import { client } from '@shared/api/client'
import { useNavigate } from 'react-router-dom'

/**
 * Синхронизированное прохождение квиза (командный/рейтинговый режим).
 * Индекс текущего вопроса и таймер берутся с СЕРВЕРА через поллинг сессии,
 * поэтому у всех игроков одинаковое время и общий переход между вопросами.
 * Счёт считается локально и сохраняется при завершении (как в соло).
 */
export function useSyncedQuiz(quizId, sessionId) {
  const navigate = useNavigate()
  const currentUser = useUser()
  const questions = useQuestions()
  const fetchQuestions = useQuestionStore((s) => s.fetchQuestions)
  const loading = useQuestionStore((s) => s.loading)
  const error = useQuestionStore((s) => s.error)

  const [serverIndex, setServerIndex] = useState(0)
  const [timeLeft, setTimeLeft] = useState(null)
  const [totalScore, setTotalScore] = useState(0)
  const [correctCount, setCorrectCount] = useState(0)
  const [submittedIndex, setSubmittedIndex] = useState(-1)
  const [votedIndex, setVotedIndex] = useState(-1)

  // Командное состояние из поллинга
  const [players, setPlayers] = useState([])
  const [teams, setTeams] = useState([])
  const [currentVotes, setCurrentVotes] = useState([])

  const startTimeRef = useRef(Date.now())
  const finishedRef = useRef(false)
  const prevIndexRef = useRef(0)
  const gameModeRef = useRef('competitive')
  const teamsRef = useRef([])
  const myTeamIdRef = useRef(null)

  const currentQ = questions[serverIndex]
  const { selectedAnswers, toggleAnswer, resetAnswers } = useAnswerSelection(
    currentQ?.questionType || 'single',
  )

  const totalQuestions = questions.length
  const maxPossibleScore = questions.reduce((sum, q) => sum + q.points, 0)

  // ----- Роли в командном режиме -----
  const myId = currentUser?.id
  const me = players.find((p) => p.user_id === myId)
  const isTeam = gameModeRef.current === 'team'
  const isLeader = !!me?.is_leader
  // Бан хранится на сервере — переживает перезагрузку/сворачивание вкладки
  const meBanned = !!me?.is_banned
  const myTeamId = me?.team_id || null
  const myTeam = teams.find((t) => t.id === myTeamId)
  const leaderAnswered = !!myTeam?.leader_answered
  myTeamIdRef.current = myTeamId

  // Аватары проголосовавших по вариантам (только моя команда)
  const voters = {}
  if (isTeam && myTeamId) {
    for (const v of currentVotes) {
      if (v.team_id !== myTeamId) continue
      for (const optIdx of v.answer_ids || []) {
        if (!voters[optIdx]) voters[optIdx] = []
        voters[optIdx].push({
          avatar: v.photo_profile || '',
          nickname: v.nickname || '',
        })
      }
    }
  }

  // Лидер «ответил» (submittedIndex) либо рядовой проголосовал (votedIndex)
  const isAnswered = isTeam
    ? isLeader
      ? submittedIndex === serverIndex
      : leaderAnswered // рядовому показываем результат, когда лидер решил
    : submittedIndex === serverIndex
  const hasVoted = votedIndex === serverIndex

  // Загрузка вопросов (одинаковый порядок у всех игроков)
  useEffect(() => {
    if (quizId) fetchQuestions(quizId)
  }, [quizId, fetchQuestions])

  const handleFinish = useCallback(() => {
    if (finishedRef.current) return
    finishedRef.current = true

    const durationSeconds = Math.round(
      (Date.now() - startTimeRef.current) / 1000,
    )

    // Командный режим: счёт = результат капитана (берём из стейта команды),
    // и он одинаков для всех участников команды. Иначе — личный счёт.
    let finalScore = totalScore
    let finalCorrect = correctCount
    if (gameModeRef.current === 'team') {
      const myTeam = teamsRef.current.find((t) => t.id === myTeamIdRef.current)
      if (myTeam) {
        finalScore = myTeam.score ?? 0
        finalCorrect = myTeam.correct ?? 0
      }
    }

    const percentScore = maxPossibleScore
      ? Math.round((finalScore / maxPossibleScore) * 100)
      : 0

    const navState = {
      quizTitle: 'Квиз',
      maxPossibleScore,
      percentScore,
      correctCount: finalCorrect,
      totalQuestions,
      totalScore: finalScore,
      durationSeconds,
      quizMode: gameModeRef.current,
      sessionId, // для таблицы результатов по группе
    }

    // Результат в общий лидерборд (БД) + результат в сессию (таблица группы)
    Promise.allSettled([
      client('/quiz-results/save', {
        method: 'POST',
        body: JSON.stringify({
          quiz_id: Number(quizId),
          score: finalScore,
          max_score: maxPossibleScore || 0,
          duration_seconds: durationSeconds,
        }),
      }),
      client(`/game/sessions/${sessionId}/result`, {
        method: 'POST',
        body: JSON.stringify({
          score: finalScore,
          max_score: maxPossibleScore || 0,
          correct_count: finalCorrect,
          duration_seconds: durationSeconds,
        }),
      }),
    ]).finally(() => {
      // игра завершена — убираем сохранённую сессию (чтобы не «восстановить» её)
      try {
        sessionStorage.removeItem(`quizSession:${quizId}`)
      } catch {
        // no-op
      }
      navigate(`/leaderboardRating/${quizId}`, { state: navState })
    })
  }, [
    maxPossibleScore,
    totalScore,
    correctCount,
    totalQuestions,
    quizId,
    sessionId,
    navigate,
  ])

  // Состояние сессии приходит по WebSocket — источник истины для индекса/таймера
  const handleState = useCallback(
    (state) => {
      if (state.game_mode) gameModeRef.current = state.game_mode
      setTimeLeft(state.time_left ?? null)
      setServerIndex(state.current_question_index ?? 0)
      setPlayers(Array.isArray(state.players) ? state.players : [])
      const t = Array.isArray(state.teams) ? state.teams : []
      setTeams(t)
      teamsRef.current = t
      setCurrentVotes(
        Array.isArray(state.current_votes) ? state.current_votes : [],
      )
      if (state.is_finished) handleFinish()
    },
    [handleFinish],
  )
  useGameSocket(sessionId, handleState)

  // При смене вопроса сервером — сбрасываем выбор ответа и флаг голоса
  useEffect(() => {
    if (prevIndexRef.current !== serverIndex) {
      prevIndexRef.current = serverIndex
      resetAnswers()
      setVotedIndex(-1)
    }
    // resetAnswers намеренно не в зависимостях (нестабильная ссылка)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [serverIndex])

  const submitAnswer = useCallback(() => {
    if (!currentQ) return

    // ---- Командный режим: рядовой только голосует (можно переголосовать) ----
    if (isTeam && !isLeader) {
      if (leaderAnswered || timeLeft === 0) return
      setVotedIndex(serverIndex)
      client(`/game/sessions/${sessionId}/vote`, {
        method: 'POST',
        body: JSON.stringify({
          question_index: serverIndex,
          answer_ids: selectedAnswers,
        }),
      }).catch(() => {})
      return
    }

    if (isAnswered) return

    const score = calculatePartialScore(
      selectedAnswers,
      currentQ.correctAnswers || [],
      currentQ.points || 0,
    )
    const fullyCorrect = checkAnswer(selectedAnswers, currentQ.correctAnswers)

    setTotalScore((p) => p + score)
    if (fullyCorrect) setCorrectCount((p) => p + 1)
    setSubmittedIndex(serverIndex)

    // ---- Командный лидер: фиксируем ответ команды + копим командный счёт ----
    if (isTeam && isLeader) {
      client(`/game/sessions/${sessionId}/team-answer`, {
        method: 'POST',
        body: JSON.stringify({
          question_index: serverIndex,
          answer_ids: selectedAnswers,
          points_earned: score,
          max_possible: maxPossibleScore || 0,
          is_correct: fullyCorrect,
        }),
      }).catch(() => {})
      return
    }

    // ---- Рейтинговый режим: сообщаем серверу о готовности к переходу ----
    client(`/game/sessions/${sessionId}/answered`, {
      method: 'POST',
      body: JSON.stringify({ question_index: serverIndex }),
    }).catch(() => {})
  }, [
    currentQ,
    isAnswered,
    isTeam,
    isLeader,
    leaderAnswered,
    timeLeft,
    selectedAnswers,
    serverIndex,
    sessionId,
    maxPossibleScore,
  ])

  const currentScore = calculatePartialScore(
    selectedAnswers,
    currentQ?.correctAnswers || [],
    currentQ?.points || 0,
  )

  return {
    questions,
    currentQ,
    currentQuestion: serverIndex,
    totalQuestions,
    isAnswered,
    loading,
    error,
    selectedAnswers,
    currentScore,
    totalScore,
    maxPossibleScore,
    timeLeft,
    toggleAnswer,
    submitAnswer,
    // командный режим
    isTeam,
    isLeader,
    voters,
    hasVoted,
    leaderAnswered,
    meBanned,
    players,
    teams,
  }
}
