import { z } from 'zod'

export const quizSchema = z.object({
  title: z.string().min(3, 'Введите название'),
  description: z.string().min(10, 'Введите описание'),
  category: z.string().min(1, 'Выберите категорию'),

  questions: z
    .array(
      z.object({
        questionText: z.string().min(1, 'Введите вопрос'),

        answers: z
          .array(
            z.object({
              text: z.string().min(1, 'Введите ответ'),
              isCorrect: z.boolean(),
            }),
          )
          .min(2, 'Минимум 2 ответа'),
      }),
    )
    .min(1, 'Добавьте хотя бы один вопрос'),
})
