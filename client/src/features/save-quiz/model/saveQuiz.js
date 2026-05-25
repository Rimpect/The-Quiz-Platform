import { quizSchema } from '../../quiz-editor/model/quiz.schema'

export const saveQuiz = async (quizData) => {
  const result = quizSchema.safeParse(quizData)

  if (!result.success) {
    throw new Error(result.error.issues[0].message)
  }

  await new Promise((resolve) => setTimeout(resolve, 1000))

  return {
    success: true,
  }
}
