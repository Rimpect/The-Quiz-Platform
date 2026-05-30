import { useState } from 'react'

export function useAnswerSelection(questionType) {
  const [selectedAnswers, setSelectedAnswers] = useState([])

  const toggleAnswer = (index) => {
    if (questionType === 'single') {
      setSelectedAnswers([index])
      return
    }

    setSelectedAnswers((prev) => {
      if (prev.includes(index)) {
        return prev.filter((item) => item !== index)
      }

      return [...prev, index].sort((a, b) => a - b)
    })
  }

  const resetAnswers = () => {
    setSelectedAnswers([])
  }

  return {
    selectedAnswers,
    toggleAnswer,
    resetAnswers,
  }
}
