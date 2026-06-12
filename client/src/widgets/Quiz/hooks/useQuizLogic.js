import { useState, useEffect } from 'react'

import { useQuestions, useQuestionStore, useQuiz } from '@entities'
import {
  calculatePartialScore,
  useAnswerSelection,
  checkAnswer,
} from '@features'
import { getFinishQuizRoute } from '@shared'
import { client } from '@shared/api/client'
import { useNavigate } from 'react-router-dom'

export const useQuizLogic = (quizId) => {
  const navigate = useNavigate()
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [isAnswered, setIsAnswered] = useState(false)
  const [totalScore, setTotalScore] = useState(0)
  const [correctCount, setCorrectCount] = useState(0)
  const [isFinished, setIsFinished] = useState(false)
  const [startTime] = useState(() => Date.now())

  const questions = useQuestions()
  const fetchQuestions = useQuestionStore((state) => state.fetchQuestions)
  const loading = useQuestionStore((state) => state.loading)
  const error = useQuestionStore((state) => state.error)
  const { quiz } = useQuiz(quizId)

  const currentQ = questions[currentQuestion]
  const { selectedAnswers, toggleAnswer, resetAnswers } = useAnswerSelection(
    currentQ?.questionType || 'single',
  )

  const currentScore = calculatePartialScore(
    selectedAnswers,
    currentQ?.correctAnswers || [],
    currentQ?.points || 0,
  )

  const maxPossibleScore = questions.reduce((sum, q) => sum + q.points, 0)
  const totalQuestions = questions.length

  useEffect(() => {
    if (quizId) {
      fetchQuestions(quizId)
    }
  }, [fetchQuestions, quizId])

  const handleSubmitAnswer = () => {
    setIsAnswered(true)
    setTotalScore((prev) => prev + currentScore)

    const isFullyCorrect = checkAnswer(selectedAnswers, currentQ.correctAnswers)
    if (isFullyCorrect) {
      setCorrectCount((prev) => prev + 1)
    }
  }

  const handleNext = () => {
    if (currentQuestion + 1 < totalQuestions) {
      setCurrentQuestion((prev) => prev + 1)
      resetAnswers()
      setIsAnswered(false)
    } else {
      setIsFinished(true)
      // Сбрасываем согласие с правилами, чтобы новое прохождение снова его запросило
      sessionStorage.removeItem(`agreed_quiz_${quizId}`)
      const percentScore = Math.round((totalScore / maxPossibleScore) * 100)
      const durationSeconds = Math.round((Date.now() - startTime) / 1000)

      // Для team/competitive идём на лидерборд, для solo на результаты
      const isTeamOrCompetitive =
        quiz?.quiz_mode === 'team' || quiz?.quiz_mode === 'competitive'

      const navState = {
        quizTitle: quiz?.title || 'Квиз',
        maxPossibleScore,
        percentScore,
        correctCount,
        totalQuestions,
        totalScore,
        durationSeconds,
        isViolated: false,
        violationsCount: 0,
        quizMode: quiz?.quiz_mode,
      }

      if (isTeamOrCompetitive) {
        // Сохраняем результат в лидерборд, затем переходим к таблице лидеров
        client('/quiz-results/save', {
          method: 'POST',
          body: JSON.stringify({
            quiz_id: Number(quizId),
            score: totalScore,
            max_score: maxPossibleScore || 0,
            duration_seconds: durationSeconds,
          }),
        })
          .catch((e) => console.error('Failed to save quiz result:', e))
          .finally(() => {
            navigate(`/leaderboardRating/${quizId}`, { state: navState })
          })
      } else {
        navigate(getFinishQuizRoute(quizId), { state: navState })
      }
    }
  }

  const handleTimeEnd = () => {
    if (!isAnswered) {
      handleSubmitAnswer()
      setTimeout(handleNext, 1000)
    } else {
      handleNext()
    }
  }

  return {
    questions,
    currentQ,
    currentQuestion,
    totalQuestions,
    isAnswered,
    isFinished,
    loading,
    error,
    selectedAnswers,
    currentScore,
    totalScore,
    correctCount,
    maxPossibleScore,

    toggleAnswer,
    handleSubmitAnswer,
    handleNext,
    handleTimeEnd,
    resetAnswers: () => {
      resetAnswers()
      setIsAnswered(false)
    },
  }
}
