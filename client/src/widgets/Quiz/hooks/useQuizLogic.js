import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuestions, useQuestionStore } from '@entities'
import {
  calculatePartialScore,
  useAnswerSelection,
  checkAnswer,
} from '@features'
import { getFinishQuizRoute } from '@shared'

export const useQuizLogic = (quizId) => {
  const navigate = useNavigate()
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [isAnswered, setIsAnswered] = useState(false)
  const [totalScore, setTotalScore] = useState(0)
  const [correctCount, setCorrectCount] = useState(0)
  const [isFinished, setIsFinished] = useState(false)

  const questions = useQuestions()
  const fetchQuestions = useQuestionStore((state) => state.fetchQuestions)
  const loading = useQuestionStore((state) => state.loading)
  const error = useQuestionStore((state) => state.error)

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
      const percentScore = Math.round((totalScore / maxPossibleScore) * 100)
      navigate(getFinishQuizRoute(quizId), {
        state: {
          quizTitle: currentQ?.title || 'Квиз',
          maxPossibleScore,
          percentScore,
          correctCount,
          totalQuestions,
          isViolated: false,
          violationsCount: 0,
        },
      })
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
