import { Button } from '@shared'
import { Save } from 'lucide-react'
import { toast } from 'sonner'

import { saveQuiz } from '../model/saveQuiz'

import { useQuizStore } from '../../quiz-editor/model/quiz.store'
import { quizSchema } from '../../quiz-editor/model/quiz.schema'

export function SaveQuiz() {
  const quiz = useQuizStore((state) => state.quiz)

  const handleSave = async () => {
    const result = quizSchema.safeParse(quiz)

    if (!result.success) {
      toast.error(result.error.issues[0].message)

      return
    }

    try {
      await saveQuiz(quiz)

      console.log(quiz)

      toast.success('Квиз сохранен')
    } catch (e) {
      toast.error(e.message || 'Ошибка сохранения')
    }
  }

  return (
    <Button
      onClick={handleSave}
      variant="black"
      size="medium"
      icon={<Save size={20} />}
    >
      Сохранить квиз
    </Button>
  )
}
