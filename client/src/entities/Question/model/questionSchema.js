import { z } from 'zod'

const questionSchemaItem = z.object({
  id: z.string(),
  quizId: z.number(),
  question: z.string(),
  questionType: z.enum(['single', 'multiple']),
  options: z.array(z.string()),
  correctAnswers: z.array(z.number()),
  points: z.number(),
  mediaUrl: z.string().nullable().optional(),
  mediaType: z.string().nullable().optional(),
  timeLimitSeconds: z.number().nullable().optional(),
})

export const questionSchema = z.array(questionSchemaItem)
