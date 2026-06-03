import { useParams } from 'react-router-dom'

import { QuizDescription } from '@widgets'
import { useQuiz } from '@entities/quiz'

export function QuizDescriptionPage() {
  const { id } = useParams()
  const { quiz, loading, error } = useQuiz(id)

  if (loading) {
    return <div>Загрузка квиза...</div>
  }

  if (error) {
    return <div>{error}</div>
  }

  if (!quiz) {
    return <div>Квиз не найден.</div>
  }

  return (
    <div>
      <QuizDescription quiz={quiz} />
    </div>
  )
}
