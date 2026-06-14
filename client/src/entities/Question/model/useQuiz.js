import { useEffect, useState } from 'react'

import { client } from '@shared/api/client'

export const useQuiz = (quizId) => {
  const [quiz, setQuiz] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!quizId) {
      setLoading(false)
      return
    }

    const fetchQuiz = async () => {
      try {
        setLoading(true)
        const response = await client(`/quizzes/${quizId}`)
        // API возвращает { data: {...}, status: "success" }
        const quizData = response?.data ?? response
        setQuiz(quizData)
        setError(null)
      } catch (err) {
        setError(err.message || 'Не удалось загрузить квиз')
        setQuiz(null)
      } finally {
        setLoading(false)
      }
    }

    fetchQuiz()
  }, [quizId])

  return { quiz, loading, error }
}
