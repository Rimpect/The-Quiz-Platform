import { Button } from '@shared'
import { Save } from 'lucide-react'
import { toast } from 'sonner'

import { quizSchema } from '../../quiz-editor/model/quiz.schema'
import { useQuizStore } from '../../quiz-editor/model/quiz.store'
import { saveQuiz } from '../model/saveQuiz'

export function SaveQuiz() {
  const quiz = useQuizStore((state) => state.quiz)
  const editQuizId = useQuizStore((state) => state.editQuizId)

  const scrollToQuestion = (index) => {
    const el = document.getElementById(`quiz-question-${index}`)
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' })
    } else {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }

  const handleSave = async () => {
    const result = quizSchema.safeParse(quiz)

    if (!result.success) {
      const issue = result.error.issues[0]
      toast.error(issue.message)
      // Прокручиваем к месту ошибки: к вопросу или наверх (общие поля)
      if (issue.path[0] === 'questions' && typeof issue.path[1] === 'number') {
        scrollToQuestion(issue.path[1])
      } else {
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
      return
    }

    // У каждого вопроса должен быть отмечен правильный ответ
    const badIndex = quiz.questions.findIndex(
      (q) => !q.answers.some((a) => a.isCorrect),
    )
    if (badIndex !== -1) {
      toast.error(`Вопрос ${badIndex + 1}: выберите правильный ответ`)
      scrollToQuestion(badIndex)
      return
    }

    try {
      const response = await saveQuiz(quiz, editQuizId)

      if (response?.status === 'pending') {
        toast.success(
          editQuizId
            ? 'Квиз отправлен на повторную модерацию'
            : 'Квиз отправлен на модерацию',
          {
            description:
              'Он появится в каталоге после проверки администратором',
            duration: 5000,
          },
        )
      } else {
        toast.success(editQuizId ? 'Квиз обновлён' : 'Квиз опубликован')
      }
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
