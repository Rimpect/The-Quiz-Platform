import { useCallback, useEffect, useRef, useState } from 'react'

import { useQuestions, useQuestionStore } from '@entities'
import {
  calculatePartialScore,
  useAnswerSelection,
  checkAnswer,
} from '@features'
import { client } from '@shared/api/client'
import { useNavigate } from 'react-router-dom'

const POLL_INTERVAL_MS = 1000

/**
 * Синхронизированное прохождение квиза (командный/рейтинговый режим).
 * Индекс текущего вопроса и таймер берутся с СЕРВЕРА через поллинг сессии,
 * поэтому у всех игроков одинаковое время и общий переход между вопросами.
 * Счёт считается локально и сохраняется при завершении (как в соло).
 */
export function useSyncedQuiz(quizId, sessionId) {
  const navigate = useNavigate()
  const questions = useQuestions()
  const fetchQuestions = useQuestionStore((s) => s.fetchQuestions)
  const loading = useQuestionStore((s) => s.loading)
  const error = useQuestionStore((s) => s.error)

  const [serverIndex, setServerIndex] = useState(0)
  const [timeLeft, setTimeLeft] = useState(null)
  const [totalScore, setTotalScore] = useState(0)
  const [correctCount, setCorrectCount] = useState(0)
  const [submittedIndex, setSubmittedIndex] = useState(-1)

  const startTimeRef = useRef(Date.now())
  const finishedRef = useRef(false)
  const prevIndexRef = useRef(0)
  const gameModeRef = useRef('competitive')

  const currentQ = questions[serverIndex]
  const { selectedAnswers, toggleAnswer, resetAnswers } = useAnswerSelection(
    currentQ?.questionType || 'single',
  )

  const totalQuestions = questions.length
  const maxPossibleScore = questions.reduce((sum, q) => sum + q.points, 0)
  const isAnswered = submittedIndex === serverIndex

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
    const percentScore = maxPossibleScore
      ? Math.round((totalScore / maxPossibleScore) * 100)
      : 0

    const navState = {
      quizTitle: 'Квиз',
      maxPossibleScore,
      percentScore,
      correctCount,
      totalQuestions,
      totalScore,
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
          score: totalScore,
          max_score: maxPossibleScore || 0,
          duration_seconds: durationSeconds,
        }),
      }),
      client(`/game/sessions/${sessionId}/result`, {
        method: 'POST',
        body: JSON.stringify({
          score: totalScore,
          max_score: maxPossibleScore || 0,
          correct_count: correctCount,
          duration_seconds: durationSeconds,
        }),
      }),
    ]).finally(() => {
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

  // Поллинг состояния сессии — источник истины для индекса и таймера
  useEffect(() => {
    if (!sessionId) return

    const poll = async () => {
      try {
        const state = await client(`/game/sessions/${sessionId}`)
        if (state.game_mode) gameModeRef.current = state.game_mode
        setTimeLeft(state.time_left ?? null)
        setServerIndex(state.current_question_index ?? 0)
        if (state.is_finished) handleFinish()
      } catch {
        // единичные ошибки поллинга игнорируем
      }
    }

    poll()
    const id = setInterval(poll, POLL_INTERVAL_MS)
    return () => clearInterval(id)
  }, [sessionId, handleFinish])

  // При смене вопроса сервером — сбрасываем выбор ответа
  useEffect(() => {
    if (prevIndexRef.current !== serverIndex) {
      prevIndexRef.current = serverIndex
      resetAnswers()
    }
    // resetAnswers намеренно не в зависимостях (нестабильная ссылка)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [serverIndex])

  const submitAnswer = useCallback(() => {
    if (!currentQ || isAnswered) return

    const score = calculatePartialScore(
      selectedAnswers,
      currentQ.correctAnswers || [],
      currentQ.points || 0,
    )
    const fullyCorrect = checkAnswer(selectedAnswers, currentQ.correctAnswers)

    setTotalScore((p) => p + score)
    if (fullyCorrect) setCorrectCount((p) => p + 1)
    setSubmittedIndex(serverIndex)

    // Сообщаем серверу — если ответили все, он сразу переключит вопрос
    client(`/game/sessions/${sessionId}/answered`, {
      method: 'POST',
      body: JSON.stringify({ question_index: serverIndex }),
    }).catch(() => {})
  }, [currentQ, isAnswered, selectedAnswers, serverIndex, sessionId])

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
  }
}
