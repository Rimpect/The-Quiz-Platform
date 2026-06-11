import { useEffect, useState } from 'react'

import { getQuizzes, getQuizById } from '../api/quizApi.js'

export function useQuizzes() {
  const [quizzes, setQuizzes] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    let canceled = false

    const fetchQuizzes = async () => {
      setLoading(true)
      setError(null)

      try {
        const data = await getQuizzes()
        if (!canceled) {
          setQuizzes(Array.isArray(data) ? data : [])
        }
      } catch (err) {
        if (!canceled) {
          setError(err.message || 'Не удалось загрузить квизы')
        }
      } finally {
        if (!canceled) {
          setLoading(false)
        }
      }
    }

    fetchQuizzes()

    return () => {
      canceled = true
    }
  }, [])

  return { quizzes, loading, error }
}

export function useQuiz(id) {
  const [quiz, setQuiz] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!id) {
      return
    }

    let canceled = false

    const fetchQuiz = async () => {
      setLoading(true)
      setError(null)

      try {
        const data = await getQuizById(id)
        if (!canceled) {
          setQuiz(data)
        }
      } catch (err) {
        if (!canceled) {
          setError(err.message || 'Квиз не найден')
        }
      } finally {
        if (!canceled) {
          setLoading(false)
        }
      }
    }

    fetchQuiz()

    return () => {
      canceled = true
    }
  }, [id])

  return { quiz, loading, error }
}
