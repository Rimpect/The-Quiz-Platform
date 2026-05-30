import { useState } from 'react'

export function useQuizPlayer() {
  const [currentQuestion, setCurrentQuestion] = useState(0)

  const [selectedAnswers, setSelectedAnswers] = useState([])

  const [isAnswered, setIsAnswered] = useState(false)

  const handleSelectAnswer = () => {}

  const handleSubmitAnswer = () => {}

  const handleNextQuestion = () => {}

  const handleSkipQuestion = () => {}

  return {
    currentQuestion,
    selectedAnswers,
    isAnswered,

    handleSelectAnswer,
    handleSubmitAnswer,
    handleNextQuestion,
    handleSkipQuestion,
  }
}
